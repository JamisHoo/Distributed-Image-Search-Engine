#!/usr/bin/env python
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
 #  Time: 15:15:10
 #  Description: 
###############################################################################

from __future__ import print_function
import socket
import functools
import pyhdfs

LISTEN_ADDR = "localhost"
LISTEN_PORT = 20003
HDFS_HOST = "localhost:50070"
HDFS_IMAGENET = "/imagenet/"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.bind((LISTEN_ADDR, LISTEN_PORT))

sock.listen(1)

hdfs_client = pyhdfs.HdfsClient(hosts = HDFS_HOST)

def process_query(query, client_sock):
    global hdfs_client
    global sock

    counter, position = query.split(":")
    block_no, offset, length = map(functools.partial(int, base = 16), position.split(","))

    image = hdfs_client.open(HDFS_IMAGENET + format(block_no, "08x"), offset = offset, length = length).read()

    client_sock.send(counter + ":" + image)

while True:
    client_sock, client_addr = sock.accept()

    try:
        buff = ""
        while True:
            buff += client_sock.recv(1024 * 1024)
            pos = buff.find("\n")
            if pos != -1:
                process_query(buff[: pos], client_sock)
                buff = buff[pos + 1:]

    except Exception as e:
        print("Connection failed. ")
        print(e)
