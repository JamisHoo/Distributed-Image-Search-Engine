/******************************************************************************
 *  Copyright (c) 2015 Jamis Hoo
 *  Distributed under the MIT license 
 *  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 *  
 *  Project: 
 *  Filename: request_handlers.js
 *  Version: 1.0
 *  Author: Jamis Hoo
 *  E-mail: hjm211324@gmail.com
 *  Date: Jul 31, 2015
 *  Time: 23:56:29
 *  Description: handle requests
 *****************************************************************************/
var path = require("path");
var fs = require("fs");
var net = require("net");


var tcp_count = 0;
var tcp_connections = [];
var tcp_hosts = [];
var tcp_hash = {};

var query_counter = 0;
var query_hash = {};

function root(query, response) {
    response.writeHead(200, { "Content-Type": "text/plain" });
    response.write("Hello I'm root. ");
    response.end();
}

function resources(pathname, response) {
    function respond_file(abs_path) {
        fs.exists(abs_path, function(exists) {
            if (exists) {
                switch (path.extname(abs_path)){
                    case ".html":
                        response.writeHead(200, { "Content-Type": "text/html" });
                        break;
                    case ".js":
                        response.writeHead(200, { "Content-Type": "text/javascript" });
                        break;
                    case ".css":
                        response.writeHead(200, { "Content-Type": "text/css" });
                        break;
                    case ".gif":
                        response.writeHead(200, { "Content-Type": "image/gif" });
                        break;
                    case ".jpg":
                        response.writeHead(200, { "Content-Type": "image/jpeg" });
                        break;
                    case ".png":
                        response.writeHead(200, { "Content-Type": "image/png" });
                        break;
                    default:
                        response.writeHead(200, { "Content-Type": "application/octet-stream" });
                }
                fs.readFile(abs_path, function(err, data) { response.end(data); });
            } else {
                console.log(abs_path + "not exists. ");
                response.writeHead(404, {"Content-Type": "text/html"});
                response.end("<h1>404 Not Found</h1> ");
            }
        });
    }

    respond_file(__dirname + pathname);
}

function search(query, response) {
    // no worker is working
    if (tcp_count == 0) {
        response.writeHead(503, { "Content-Type": "text/plain" });
        response.write("No worker is working. ");
        response.end();
        return;
    }
    
    var query_valid = false;
    // keywords non-empty
    if ("keywords" in query) {
        // extract keywords
        var keywords = query["keywords"].replace(/\s/g, '');
        
        // if keywords only consists of whitespaces
        if (keywords.replace(/\+/g, '').length != 0) {
            // send query to worker
            rand = Math.floor(Math.random() * tcp_count);
            worker = tcp_connections[rand];
            worker.write(query_counter + ":" + keywords + "\n", "UTF8");
            
            query_hash[query_counter] = response;
            ++query_counter;
            
            query_valid = true;
        }
    }
    
    if (!query_valid) {
        response.writeHead(200, { "Content-Type": "text/plain" });
        response.write("Hello I'm search. ");
        response.end();
    }
}

function newworker(query, response) {

    function create_worker(worker_addr, worker_port) {
        var worker = new net.Socket();

        worker.connect(worker_port, worker_addr, function() {
            var worker_host = worker_addr + ":" + worker_port;
            tcp_connections[tcp_count] = worker;
            tcp_hosts[tcp_count] = worker_host;
            tcp_hash[worker_host] = tcp_count;
            ++tcp_count;

            console.log("new connection: ");
            console.log(worker_host);
            console.log("tcp_count");
            console.log(tcp_count);
            console.log("tcp connections:");
            console.log(tcp_connections.length);
            console.log("tcp hosts: ");
            console.log(tcp_hosts);
            console.log("tcp hash: ");
            console.log(tcp_hash);
        });

        worker.on("error", function(err) { console.log(err); });
        worker.on("timeout", function(timeout) { console.log(timeout); });

        worker.on("data", function(data) {
            console.log("Receive: " + data); 
            
            var colon_index = data.toString().indexOf(":");
            if (colon_index == -1) 
                return;

            var query_index = parseInt(data.toString().substring(0, colon_index));
            var query_result = data.toString().substring(colon_index + 1);

            var response = query_hash[query_index];
            if (response) {

                // TODO: for test
                // read html 
                var html_content = fs.readFileSync("static/index.html");
                response.writeHead(200, { "Content-Type": "text/html" });
                response.write(html_content);
                response.end()
                return;


                response.writeHead(200, { "Content-Type": "text/plain" });
                response.write(query_result);
                response.end();
                delete query_hash[query_index];
            }
        });

        worker.on("close", function() {
            var worker_host = worker_addr + ":" + worker_port;
            var index = tcp_hash[worker_host];

            if (!(index >= 0)) 
                return;

            delete tcp_connections[index];
            delete tcp_hosts[index];
            delete tcp_hash[worker_host];

            --tcp_count;
            if (index != tcp_count) {
                tcp_connections[index] = tcp_connections[tcp_count];
                delete tcp_connections[tcp_count];
                tcp_hosts[index] = tcp_hosts[tcp_count];
                delete tcp_connections[tcp_count];
                tcp_hash[tcp_hosts[tcp_count]] = index;
            }

            console.log("Connection closed. ");
            console.log(worker_host);
            console.log("tcp_count");
            console.log(tcp_count);
            console.log("tcp connections:");
            console.log(tcp_connections.length);
            console.log("tcp hosts: ");
            console.log(tcp_hosts);
            console.log("tcp hash: ");
            console.log(tcp_hash);
        });
    }
    
    // new worker with address and port provided
    if ("addr" in query && "port" in query) {
        var worker_host = query["addr"] + ":" + query["port"];

        // new worker 
        if (!(worker_host in tcp_hash)) {
            create_worker(query["addr"], query["port"]);

            response.writeHead(200, { "Content-Type": "text/plain" });
            response.write("Try to connect to " + worker_host);
            response.end();
        // worker alrady exists
        } else {
            response.writeHead(400, { "Content-Type": "text/plain" });
            response.write("Worker " + worker_host + " already exists. ");
            response.end();
        }
    // lack of address or port
    } else {
        response.writeHead(400, { "Content-Type": "text/plain" });
        response.write("Address or port isn't provided. ");
        response.end();
    }
}

exports.root = root;
exports.resources = resources;
exports.search = search;
exports.newworker = newworker;
