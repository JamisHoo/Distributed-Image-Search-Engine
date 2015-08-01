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
 *  Description: 
 *****************************************************************************/

var server = require("./server");
var router = require("./router");
var request_handlers = require("./request_handlers");

var handle ={}
handle["/"] = request_handlers.root;
handle["/static"] = request_handlers.resources;
handle["/search"] = request_handlers.search;
handle["/newworker"] = request_handlers.newworker;

server.start(router.route, handle);
