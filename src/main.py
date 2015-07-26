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


# load inverted index
# TODO: broadcast this?
inverted_index = index.load_index(INDEX_FILE)


# Create a StreamingContext and batch interval of 1 second
sc = SparkContext(appName = "ImageSearch")
ssc = StreamingContext(sc, 1)

# Create a DStream that will connect to hostname:port, like localhost:9999
# each line is a query, which contains some keywords spliting with spaces
# assuming line is not empty
lines = ssc.socketTextStream(QUERY_ADDR, QUERY_PORT)

keywords = lines.map(lambda line: line.split())

str_keywords = keywords.map(lambda keys: ",".join(keys))
bytes_keywords = str_keywords.map(lambda s: str.encode(str(s)))

bytes_keywords.pprint()

#keywords.pprint()
bytes_keywords.foreachRDD(lambda rdd: rdd.foreachPartition(send_result.send))


# Start the computation
ssc.start()             
# Wait for the computation to terminate
ssc.awaitTermination()  
