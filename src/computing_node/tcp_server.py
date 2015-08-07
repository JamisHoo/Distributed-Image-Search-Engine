#!/usr/bin/env python3
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: Distributed Image Search Engine
 #  Filename: tcp_server.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hoojamis@gmail.com
 #  Date: Aug  2, 2015
 #  Time: 15:09:32
 #  Description: tcp echo server
###############################################################################

import socketserver

class EchoTCPServer(socketserver.BaseRequestHandler):
    def setup(self):
        print('{}:{} connected'.format(*self.client_address))

    def finish(self):
        print('{}:{} disconnected'.format(*self.client_address))

    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            if not self.data:
                break

            self.request.sendall(self.data)

