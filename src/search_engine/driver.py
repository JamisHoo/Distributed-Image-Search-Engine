#!/usr/bin/env python
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: driver.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hjm211324@gmail.com
 #  Date: Jul 30, 2015
 #  Time: 21:27:03
 #  Description: 
###############################################################################

from __future__ import print_function

from pyspark import SparkContext
from pyspark.streaming import StreamingContext

import time

from engine import SearchEngine

search_index_path = "index"
query_host = ("localhost", 10001)
result_host = ("localhost", 10002)

# load inverted index
search_engine = SearchEngine(result_host)
search_engine.load_index(search_index_path)

# creating a StreamingContext and batch interval 
sc = SparkContext(appName = "ImageSearch")
ssc = StreamingContext(sc, 1)

search_engine_broadcast = sc.broadcast(search_engine)

# Create a DStream that will connect to hostname:port, like localhost:9999
# each line is a query, which contains some keywords spliting with spaces
# assuming line is not empty
lines = ssc.socketTextStream(query_host[0], query_host[1])

# convert keywords to list
keywords = lines.map(lambda line: line.split())

print("*" * 50)
keywords.pprint()
                                                                                
# do search
# result is list of tuples of position
def search_func(x):
    search_engine_value = search_engine_broadcast.value
    return search_engine_value.search(x)

search_result = keywords.map(search_func)

# convert result to ascii string
str_result = search_result.map(lambda x: str.encode(",".join([ format(z, "x") for y in x for z in y ])))

print(("*" * 50 + "\n") * 10)
#str_result.pprint()
print(time.time())
                                                                                
# send result to result receiving server
def send_func(x):
    search_engine_value = search_engine_broadcast.value
    return search_engine_value.send_result(x)
str_result.foreachRDD(lambda rdd: rdd.foreachPartition(send_func))


# Start the computation
ssc.start()
# Wait for the computation to terminate
ssc.awaitTermination()
