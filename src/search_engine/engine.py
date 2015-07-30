#!/usr/bin/env python
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: engine.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hjm211324@gmail.com
 #  Date: Jul 30, 2015
 #  Time: 20:59:01
 #  Description: 
###############################################################################

import socket
import time

class SearchEngine(object):
    def __init__(self, result_host):
        self.index = dict()
        self.result_host = result_host
        self.result_socket = None

    # each line of index file is in format:
    # keyword1,keyword2,keyword3,...,keywordn[tab]bn1,off1,len1,bn2,off2,len2,...,bnn,offn,lenn
    # bn is block No.
    # off is offset
    # len is length
    def load_index(self, file_path):
        with open(file_path) as file_handler:
            for line in file_handler:
                keywords = line[: line.find("\t")].split(",")
                positions = []
                poss = [ int(x, 16) for x in line[line.find("\t") + 1: -1].split(",") ]
                for i in range(0, len(poss), 3):
                    positions.append((poss[i], poss[i + 1], poss[i + 2]))
                for keyword in keywords:
                    if keyword not in self.index:
                        self.index[keyword] = positions
                    else:
                        self.index[keyword].extend(positions)

    def connect_to_result_server(self):
        try:
            self.result_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.result_socket.connect(self.result_host)
        except Exception as e:
            print e

    def send_result(self, rdd_iter):
        print(time.time())
        if self.result_socket == None:
            self.connect_to_result_server()

        try:
            for record in rdd_iter:
                self.result_socket.sendall(record)
        except Exception as e:
            print e

    def search(self, keywords):
        result = None
        for keyword in keywords:
            inter_result = self.index.get(keyword)
            
            if inter_result == None:
                break

            if result == None:
                result = set(inter_result)
            else:
                result &= set(inter_result)

            if result == None:
                return list()

        if result == None:
            return list()
        else:
            return list(result)


