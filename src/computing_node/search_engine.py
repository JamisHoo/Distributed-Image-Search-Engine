#!/usr/bin/env python3
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: search_engine.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hoojamis@gmail.com
 #  Date: Aug  2, 2015
 #  Time: 14:41:10
 #  Description: 
###############################################################################
from http.server import BaseHTTPRequestHandler 
import re

class SearchEngine(BaseHTTPRequestHandler):
    path_pattern = re.compile("^/[^?]*\?keywords=(.+)$", flags = re.IGNORECASE)
    index = dict()

    @staticmethod
    def load_index(file_path):
        with open(file_path) as file_handler:
            for line in file_handler:
                keywords = line[: line.find("\t")].split(",")
                positions = []
                poss = [ int(x, 16) for x in line[line.find("\t") + 1: -1].split(",") ]
                for i in range(0, len(poss), 3):
                    positions.append((poss[i], poss[i + 1], poss[i + 2]))
                for keyword in keywords:
                    if keyword not in SearchEngine.index:
                        SearchEngine.index[keyword] = positions
                    else:
                        SearchEngine.index[keyword].extend(positions)

    def do_GET(self):
        match_obj = SearchEngine.path_pattern.match(self.path)

        if not match_obj or len(match_obj.groups()) == 0:
            self.send_reject()
        else:
            result = self.search_keywords(filter(None, match_obj.groups()[0].split("+")));
            result_str = ";".join(",".join(format(y, "x") for y in x) for x in result)

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(result_str.encode("ascii"))

    def send_reject(self):
        self.send_response(400)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        messages = [
            "Format of request URL: /?keywords=[keyword]+[keyword]+...+[keyword]",
            ""
            "e.g."
            "http://192.168.1.100:10005/keywords=dog+cat",
            "http://59.66.130.35:10005/keywrds=food"
        ]
        self.wfile.write("\n".join(messages).encode("utf-8"))
    
    def search_keywords(self, keywords):
        result = None
        for keyword in keywords:
            inter_result = SearchEngine.index.get(keyword)
            
            if inter_result == None:
                break

            if result == None:
                result = set(inter_result)
            else:
                result &= set(inter_result)

            if result == None:
                return list()

        if result == None:
            return list()
        else:
            return list(result) 


