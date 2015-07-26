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

import index
import send_result

INDEX_FILE = "../imagenet/index"
QUERY_ADDR = "localhost"
QUERY_PORT = 20000


# Create a StreamingContext and batch interval of 1 second
sc = SparkContext(appName = "ImageSearch")
ssc = StreamingContext(sc, 1)

# load inverted index
# and broadcast to each word node
inverted_index_var = sc.broadcast(index.load_index(INDEX_FILE))

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
str_result = search_result.map(lambda x: str.encode(str(x)))
    
str_result.pprint()

#keywords.pprint()
str_result.foreachRDD(lambda rdd: rdd.foreachPartition(send_result.send))


# Start the computation
ssc.start()             
# Wait for the computation to terminate
ssc.awaitTermination()  
