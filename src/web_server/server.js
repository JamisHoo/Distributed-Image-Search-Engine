/******************************************************************************
 *  Copyright (c) 2015 Jamis Hoo
 *  Distributed under the MIT license 
 *  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 *  
 *  Project:
 *  Filename: server.js
 *  Version: 1.0
 *  Author: Jamis Hoo
 *  E-mail: hjm211324@gmail.com
 *  Date: Jul 31, 2015
 *  Time: 23:56:29
 *  Description: server start, send request to router
 *****************************************************************************/

var http = require("http");
var url = require("url");
var querystring = require("querystring");

function start(route, handle) {
    function onRequest(request, response) { 
        var urlobj = url.parse(request.url)
        var pathname = urlobj.pathname
        var query = querystring.parse(urlobj.query)

        console.log("Request for " + pathname + " received.");

        // send to router
        route(handle, pathname, query, response);
    }

    http.createServer(onRequest).listen(8888);
    console.log("Server has started.");
}

exports.start = start;
