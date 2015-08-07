#!/usr/bin/env python3
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: Distributed Image Search Engine
 #  Filename: new_process.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hjm211324@gmail.com
 #  Date: Aug  2, 2015
 #  Time: 20:39:46
 #  Description: create new processes
###############################################################################

from http.server import HTTPServer
import time
import socketserver
import urllib.request

from read_hdfs import ImageServer
from tcp_server import EchoTCPServer

# create a new http server
def new_http_process(addr, port):
    my_server = HTTPServer((addr, port), ImageServer)
    print(time.asctime(), "HTTP Server Starts - %s:%s" % (addr, port))

    try:
        my_server.serve_forever()
    except KeyboardInterrupt:
        pass

    my_server.server_close()
    print(time.asctime(), "HTTP Server Stops - %s:%s" % (addr, port))

# crate master detecting process
def new_master_detect_process(master_addr, master_port, local_addr, http_ports, tcp_port):
    while True:
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            break

        for http_port in http_ports:
            url = "http://%s:%s/new_storage_node/?addr=%s&http_port=%s&tcp_port=%s" % \
                (master_addr, str(master_port), local_addr, str(http_port), str(tcp_port))
            try:
                urllib.request.urlopen(url)
            except Exception:
                pass

# create echo TCP server
def new_tcp_process(addr, port):
    socketserver.TCPServer.allow_reuse_address = True

    print(time.asctime(), "TCP Server Starts - %s:%s" % (addr, port))
    server = socketserver.TCPServer((addr, port), EchoTCPServer)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print(time.asctime(), "TCP Server Stops - %s:%s" % (addr, port))



