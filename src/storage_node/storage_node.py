#!/usr/bin/env python3
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: storage_node.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hjm211324@gmail.com
 #  Date: Aug  2, 2015
 #  Time: 20:39:37
 #  Description: 
###############################################################################

import multiprocessing

from new_process import *


hdfs_host = "localhost:50070"
hdfs_image_path = "/imagenet/"
local_addr = "192.168.1.100"
tcp_port = 10010
http_ports = [ 10011, 10012, 10013, 10014 ]

master_addr = "192.168.1.102"
master_port = 3000

if __name__ == "__main__":
    ImageServer.init(hdfs_host, hdfs_image_path) 

    # processes set
    processes = []

    # TCP server
    processes.append(multiprocessing.Process(target = new_tcp_process, \
        args = (local_addr, tcp_port)))
    processes[-1].start()

    # HTTP servers
    for http_port in http_ports:
        processes.append(multiprocessing.Process(target = new_http_process, \
            args = (local_addr, http_port)))
        processes[-1].start()

    # master detecting process
    processes.append(multiprocessing.Process(target = new_master_detect_process, \
        args = (master_addr, master_port, local_addr, http_ports, tcp_port)))
    processes[-1].start()

    for process in processes:
        try:
            process.join()
        except KeyboardInterrupt:
            process.join()
