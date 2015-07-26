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

SPARK_HOME=~/Desktop/spark-1.4.0-bin-hadoop2.6/
SRC_DIR=src/

cd ${SRC_DIR}; ${SPARK_HOME}/bin/spark-submit main.py
