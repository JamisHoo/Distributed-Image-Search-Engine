#!/usr/bin/env python
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: index.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hjm211324@gmail.com
 #  Date: Jul 26, 2015
 #  Time: 19:23:08
 #  Description: 
###############################################################################

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
