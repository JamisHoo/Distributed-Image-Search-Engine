#!/usr/bin/env python3
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: computing_node.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hoojamis@gmail.com
 #  Date: Aug  2, 2015
 #  Time: 08:32:02
 #  Description: 
###############################################################################

import multiprocessing

from new_process import *




search_index_path = "index"

local_addr = "0.0.0.0"
tcp_port = 10000
http_ports = [ 10001, 10002 , 10003, 10004 ]

master_addr = "localhost"
master_port = 3000



if __name__ == "__main__":
    SearchEngine.load_index(search_index_path)

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
