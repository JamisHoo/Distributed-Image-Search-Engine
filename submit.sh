#!/bin/sh
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: submit.sh 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hjm211324@gmail.com
 #  Date: Jul 26, 2015
 #  Time: 19:10:20
 #  Description: 
###############################################################################

# run spark job locally
SPARK_HOME=$(realpath ~/Desktop/spark-1.4.0-bin-hadoop2.6/)
SRC_PATH=$(realpath src/search_engine/driver.py)
PY_FILES=${SRC_PATH},$(realpath src/search_engine/engine.py)
INDEX_DIR=$(realpath imagenet/)

cd $INDEX_DIR; ${SPARK_HOME}/bin/spark-submit --py-files ${PY_FILES} $SRC_PATH



: '
WORKING_FILES=$(realpath imagenet/index)
export HADOOP_CONF_DIR=$(realpath ~/Desktop/hadoop-2.7.1)
cd ${SRC_DIR}; \
${SPARK_HOME}/bin/spark-submit \
--master yarn-cluster \
--queue default \
--files $WORKING_FILES \
main.py
'
