/******************************************************************************
 *  Copyright (c) 2015 Jamis Hoo
 *  Distributed under the MIT license 
 *  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 *  
 *  Project: 
 *  Filename: index.js
 *  Version: 1.0
 *  Author: Jamis Hoo
 *  E-mail: hjm211324@gmail.com
 *  Date: Jul 31, 2015
 *  Time: 23:56:29
 *  Description: main
 *****************************************************************************/

var server = require("./server");
var router = require("./router");
var request_handlers = require("./request_handlers");

var handle ={}
handle["/static"] = request_handlers.resources;
handle["/newcomputingnode"] = request_handlers.new_computing_node;
handle["/newstoragenode"] = request_handlers.new_storage_node;
handle["/overview"] = request_handlers.overview;

server.start(router.route, handle);
