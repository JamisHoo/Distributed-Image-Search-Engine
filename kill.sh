#!/bin/sh
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: kill.sh 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hjm211324@gmail.com
 #  Date: Jul 27, 2015
 #  Time: 09:25:39
 #  Description: kill all accepted and running jobs of yarn
###############################################################################

HADOOP_HOME=$(realpath ~/Desktop/hadoop-2.7.1)

tasks=$(${HADOOP_HOME}/bin/yarn application -list | grep -o "application_[0-9]\+_[0-9]\{4\}")

for i in $tasks; do
    ${HADOOP_HOME}/bin/yarn application -kill $i
done

