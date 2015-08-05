#!/usr/bin/env python3
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: deploy_computing_nodes.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hoojamis@gmail.com
 #  Date: Aug  4, 2015
 #  Time: 23:14:53
 #  Description: 
###############################################################################

import pysftp

hosts = [ 
    # address, username, password, number of computing node processes
    ("101.200.184.227", "root", "Hahehi1234", 3),
]

master_addr = "59.66.130.35"
master_port = 3000

for host in hosts:
    with pysftp.Connection(host[0], username=host[1], password=host[2]) as sftp:
        # config basic environment
        sftp.put("auto_config.sh")
        sftp.execute("sh auto_config.sh 2>&1 | tee auto_deploy_log")
        # update computing node environment
        sftp.execute("rm -f auto_computing_node.sh")
        sftp.put("auto_computing_node.sh")
        sftp.execute("sh auto_computing_node.sh %s %s %s %s 2>&1 | tee auto_deploy_log" % (host[0], host[3], master_addr, master_port))
        sftp.execute("cd Distributed-Image-Search-Engine-ds/src/computing_node; tmux new -d -s computing_nodes")
        sftp.execute("tmux send -t computing_nodes.0 ./computing_node.py ENTER")
