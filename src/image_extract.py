#!/usr/bin/env python3
###############################################################################
 #  Copyright (c) 2015 Jamis Hoo
 #  Distributed under the MIT license 
 #  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 #  
 #  Project: 
 #  Filename: image_extract.py 
 #  Version: 1.0
 #  Author: Jamis Hoo
 #  E-mail: hjm211324@gmail.com
 #  Date: Jul 27, 2015
 #  Time: 22:26:51
 #  Description: accecpt HTTP Get request 
 #               extract image from HDFS
 #               send response to client
###############################################################################
from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import pyhdfs
import time

hostName = "0.0.0.0"
hostPort = 10005

hdfs_image_path = "/imagenet/"
hdfs_host = "localhost:50070"

path_pattern = re.compile("^/[^?]*\?block_no=([0-9a-f]*)&offset=([0-9a-f]*)&length=([0-9a-f]+)$", flags = re.IGNORECASE);

hdfs_client = pyhdfs.HdfsClient(hosts = hdfs_host)


class ImageServer(BaseHTTPRequestHandler):

    def do_GET(self):
        global path_pattern

        match_obj = path_pattern.match(self.path)
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
        global hdfs_client

        block_no = int(signature[0], 16)
        offset = int(signature[1], 16)
        length = int(signature[2], 16)

        image = hdfs_client.open(hdfs_image_path + format(block_no, "08x"), offset = offset, length = length).read()

        return image



myServer = HTTPServer((hostName, hostPort), ImageServer)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))

