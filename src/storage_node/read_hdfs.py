#!/usr/bin/env python3
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: read_hdfs.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hjm211324@gmail.com
 #  Date: Aug  2, 2015
 #  Time: 20:39:31
 #  Description: 
###############################################################################
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import pyhdfs
import time

class ImageServer(BaseHTTPRequestHandler):
    path_pattern = re.compile("^/[^?]*\?block_no=([0-9a-f]*)&offset=([0-9a-f]*)&length=([0-9a-f]+)$", flags = re.IGNORECASE);
    hdfs_client = None
    hdfs_image_path = None

    @staticmethod
    def init(hdfs_host, hdfs_image_path):
        ImageServer.hdfs_client = pyhdfs.HdfsClient(hosts = hdfs_host)
        ImageServer.hdfs_image_path = hdfs_image_path
    
    def do_GET(self):
        if not (ImageServer.hdfs_image_path and ImageServer.hdfs_client):
            self.send_reject()
            return

        match_obj = ImageServer.path_pattern.match(self.path)
        if not match_obj or len(match_obj.groups()) != 3:
            self.send_reject()
        else:
            self.send_image(match_obj.groups())

    def send_reject(self):
        self.send_response(400)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        messages = [
            "Format of request URL: /?block_no=[hex]&offset=[hex]&length=[hex] ",
            "[hex] is a number in hexadecimal without leading 0x, case insensitive. ",
            "",
            "e.g.",
            "http://192.168.1.100:10005/?block_no=4&offset=214428b48&length=d282",
            "http://59.66.130.35:10005/?block_no=1&offset=20adb4722&length=3239c"
        ]
        self.wfile.write("\n".join(messages).encode("utf-8"))

    def send_image(self, signature):
        image = self.extract_image(signature)

        self.send_response(200)
        self.send_header("Content-type", "image/jpeg")
        self.end_headers()
        self.wfile.write(image)

    def extract_image(self, signature):
        block_no = int(signature[0], 16)
        offset = int(signature[1], 16)
        length = int(signature[2], 16)

        image = ImageServer.hdfs_client.open(ImageServer.hdfs_image_path + format(block_no, "08x"), offset = offset, length = length).read()

        return image
