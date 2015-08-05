#!/bin/sh
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: auto_computing_node.sh 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hoojamis@gmail.com
 #  Date: Aug  5, 2015
 #  Time: 20:22:04
 #  Description: 
###############################################################################

if [ "$EUID" -ne 0 ]; then
    echo Not root.
    exit 1
fi

if (($# != 4)); then
    exit 1
fi


NODE_ADDR=$1
NODE_NUM_PORTS=$2
MASTER_ADDR=$3
MASTER_PORT=$4

# install computing node
rm -rf Distributed-Image-Search-Engine-ds/
wget http://test-10001818.file.myqcloud.com/Distributed-Image-Search-Engine-ds.zip
unzip Distributed-Image-Search-Engine-ds.zip > /dev/null
rm Distributed-Image-Search-Engine-ds.zip

cd Distributed-Image-Search-Engine-ds/src/computing_node/
wget http://test-10001818.file.myqcloud.com/index

# substitude computing node running parameters
line_no=$(grep -n "local_addr = " computing_node.py | cut -f1 -d:)
sed -i "${line_no}s/.*/local_addr\ =\ \\\"${NODE_ADDR}\\\"/" computing_node.py

line_no=$(grep -n "master_addr = " computing_node.py | cut -f1 -d:)
sed -i "${line_no}s/.*/master_addr\ =\ \\\"${MASTER_ADDR}\\\"/" computing_node.py

line_no=$(grep -n "master_port = " computing_node.py | cut -f1 -d:)
sed -i "${line_no}s/.*/master_port\ =\ ${MASTER_PORT}/" computing_node.py

START_PORT=10001
PORTS=""
for ((i = 0; i < $NODE_NUM_PORTS; ++i)); do
    PORTS="$PORTS$((START_PORT + i)), "
done
PORTS="[ $PORTS ]"

echo $PORTS

line_no=$(grep -n "http_ports = " computing_node.py | cut -f1 -d:)
sed -i "${line_no}s/.*/http_ports\ =\ ${PORTS}/" computing_node.py



