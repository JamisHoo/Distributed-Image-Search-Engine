#!/usr/bin/env python
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: send_result.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hjm211324@gmail.com
 #  Date: Jul 26, 2015
 #  Time: 20:53:22
 #  Description: 
###############################################################################

import socket

RESULT_ADDR = "localhost"                                                       
RESULT_PORT = 20001

def send(rdd_iter):
    send.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send.sock.connect((RESULT_ADDR, RESULT_PORT))

    try:
        for record in rdd_iter:
            send.sock.send(record)
    except Exception as e:
        print "Disconnect"
        print e

    send.sock.close()


