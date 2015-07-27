#!/usr/bin/env python3
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: image_extract.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hjm211324@gmail.com
 #  Date: Jul 27, 2015
 #  Time: 22:26:51
 #  Description: 
###############################################################################

import functools
import time
import socket
import asyncio
import threading
from queue import Queue
import pyhdfs


LISTEN_ADDR = "localhost"
LISTEN_PORT = 20003

RESULT_RECEIVE_ADDR = "localhost"
RESULT_RECEIVE_PORT = 20004

HDFS_HOST = "localhost:50070"                                                   
HDFS_IMAGENET = "/imagenet/"

# TODO: test with more threads
N_THREADS = 1


result_receive_sock = None
result_receive_sock_lock = None
task_queue = None
hdfs_client = None

# extract image and send to result receiver
def extractFromHdfs(task):
    # block No, offset and length determine an image
    block_no, offset, length = map(functools.partial(int, base = 16), task.split(","))

    # access hdfs
    image = hdfs_client.open(HDFS_IMAGENET + format(block_no, "08x"), offset = offset, length = length).read()

    print("get image length of", len(image))

    with result_receive_sock_lock:
        # send
        result_receive_sock.send(format(len(image), "08x").encode("ascii") + image)


# thread try to get task from queue
def thread_worker():
    while True:
        task = task_queue.get()
        image = extractFromHdfs(task)
        task_queue.task_done()

# accept TCP connections, receive data, put data into task queue
class ImageExtractor(asyncio.Protocol):
    def __init__(self):
        self._buff = ""

    # new connections
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    # process received data
    def data_received(self, data):
        print("data received", len(data))
        self._buff += data.decode("ascii")

        # data is splited with \n
        pos = self._buff.find("\n")
        while pos != -1:
            line = self._buff[: pos]
            print("Line: ", line)
            task_queue.put(line)

            self._buff = self._buff[pos + 1: ]
            pos = self._buff.find("\n")


# initialize connection to result receiving peer
result_receive_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
result_receive_sock.connect((RESULT_RECEIVE_ADDR, RESULT_RECEIVE_PORT))
result_receive_sock_lock = threading.Lock()


# initialize hdfs client
hdfs_client = pyhdfs.HdfsClient(hosts = HDFS_HOST) 



# initialize multithread and queue
task_queue = Queue()
for i in range(N_THREADS):
    t = threading.Thread(target = thread_worker)
    t.daemon = True
    t.start()


# initialize accept server
loop = asyncio.get_event_loop()
# each client connection will create a new protocol instance
coro = loop.create_server(ImageExtractor, LISTEN_ADDR, LISTEN_PORT)
server = loop.run_until_complete(coro)
# serve requests until CTRL+c is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass



# close the accept server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

# close connection to result receiving server
result_receive_sock.close()
