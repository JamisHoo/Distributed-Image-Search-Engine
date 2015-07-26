#!/usr/bin/env python
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: main.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hjm211324@gmail.com
 #  Date: Jul 26, 2015
 #  Time: 18:50:24
 #  Description: 
###############################################################################

from __future__ import print_function

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

import socket

INDEX_FILE = "../imagenet/index"

QUERY_ADDR = "localhost"
QUERY_PORT = 20000

RESULT_ADDR = "localhost"                                                       
RESULT_PORT = 20001

def send_result(rdd_iter):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((RESULT_ADDR, RESULT_PORT))

    try:
        for record in rdd_iter:
            sock.send(record)
    except Exception as e:
        print("Disconnect")
        print(e)

    sock.close()

def load_index(index_filename):
    inverted_index = dict()

    file_handler = open(index_filename)
    
    for line in file_handler:
        keywords = line[: line.find("\t")].split(",")

        positions = []
        poss = [ int(x, 16) for x in line[line.find("\t") + 1: -1].split(",") ]
        for i in range(0, len(poss), 3):
            positions.append((poss[i], poss[i + 1], poss[i + 2]))

        for keyword in keywords:
            if keyword not in inverted_index:
                inverted_index[keyword] = positions
            else:
                inverted_index[keyword].extend(positions)

    return inverted_index

# Create a StreamingContext and batch interval of 1 second
sc = SparkContext(appName = "ImageSearch")
ssc = StreamingContext(sc, 1)

# load inverted index
# and broadcast to each word node
inverted_index_var = sc.broadcast(load_index(INDEX_FILE))

# Create a DStream that will connect to hostname:port, like localhost:9999
# each line is a query, which contains some keywords spliting with spaces
# assuming line is not empty
lines = ssc.socketTextStream(QUERY_ADDR, QUERY_PORT)

keywords = lines.map(lambda line: line.split())

def search(keywords):
    inverted_index = inverted_index_var.value

    print("*" * 50)
    print(keywords)
    print("*" * 50)

    result = None

    for keyword in keywords:
        # intermediate result of this keyword
        inter_result = inverted_index.get(keyword)
        
        # cannot find this keyword
        if inter_result == None:
            break
        
        # merge result of each keyword
        if result == None:
            result = set(inter_result)
        else:
            result &= set(inter_result)


    return list(result)

search_result = keywords.map(search)
# str_result = search_result.map(lambda x: str.encode(str(x)))
str_result = search_result.map(lambda x: str.encode(",".join([ format(z, "x") for y in x for z in y ])))
    
str_result.pprint()

#keywords.pprint()
str_result.foreachRDD(lambda rdd: rdd.foreachPartition(send_result))


# Start the computation
ssc.start()             
# Wait for the computation to terminate
ssc.awaitTermination()  
