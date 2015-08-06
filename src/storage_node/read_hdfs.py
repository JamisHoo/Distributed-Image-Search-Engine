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
import os
import pyhdfs
import time

class ImageServer(BaseHTTPRequestHandler):
    path_pattern = re.compile("^/[^?]*\?block_no=([0-9a-f]*)&offset=([0-9a-f]*)&length=([0-9a-f]+)$", flags = re.IGNORECASE);
    hdfs_client = None
    hdfs_image_path = None
    local_fs_paths = None
    
    def __init__(self, *args):
        self.local_fs_client = dict()
        BaseHTTPRequestHandler.__init__(self, *args)

    @staticmethod
    def init(hdfs_host, hdfs_image_path, local_paths):
        if hdfs_host and hdfs_image_path:
            ImageServer.hdfs_client = pyhdfs.HdfsClient(hosts = hdfs_host)
            ImageServer.hdfs_image_path = hdfs_image_path
        elif local_paths:
            ImageServer.local_fs_paths = local_paths
    
    def do_GET(self):
        if not (ImageServer.hdfs_image_path and ImageServer.hdfs_client or ImageServer.local_fs_paths):
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
            "http://59.66.130.16:10011/?block_no=d&offset=4e8d97f65&length=1ea02",
            "http://59.66.130.16:10011/?block_no=e&offset=7ce740544&length=31517",
        ]
        self.wfile.write("\n".join(messages).encode("utf-8"))

    def send_image(self, signature):
        image = self.extract_image(signature)

        self.send_response(200)
        self.send_header("Content-type", "image/jpeg")
        self.end_headers()
        self.wfile.write(image)

    def extract_image(self, signature):
        block_no = format(int(signature[0], 16), "08x")
        offset = int(signature[1], 16)
        length = int(signature[2], 16)

        if ImageServer.hdfs_client:
            image = ImageServer.hdfs_client.open(ImageServer.hdfs_image_path + block_no, offset = offset, length = length).read()
        elif ImageServer.local_fs_paths:
            if block_no not in self.local_fs_client:
                for path in ImageServer.local_fs_paths:
                    if os.path.exists(os.path.join(path, block_no)):
                        self.local_fs_client[block_no] = open(os.path.join(path, block_no), "rb")
                        break
                else:
                    return "File not found. ".encode("ascii")

            image_file_handle = self.local_fs_client[block_no];
            image_file_handle.seek(offset)
            image = image_file_handle.read(length)
        else:
            image = "No hdfs or local fs clients. ".encode("ascii")

        return image
