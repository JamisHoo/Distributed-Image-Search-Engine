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

var computing_count = 0;
var computing_connections = [];
var computing_hosts = [];
var computing_hash = {};

var storage_count = 0;
var storage_connections = [];
var storage_hosts = [];
var storage_hash = {};


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
                console.log(abs_path + " not exists. ");
                response.writeHead(404, {"Content-Type": "text/html"});
                response.end("<h1>404 Not Found</h1> ");
            }
        });
    }

    respond_file(__dirname + pathname);
}

function new_computing_node(query, response) {

    function create_worker(worker_addr, worker_port) {
        var worker = new net.Socket();

        worker.connect(worker_port, worker_addr, function() {
            var worker_host = worker_addr + ":" + worker_port;
            computing_connections[computing_count] = worker;
            computing_hosts[computing_count] = worker_host;
            computing_hash[worker_host] = computing_count;
            ++computing_count;

            /*
            console.log("new connection: ");
            console.log(worker_host);
            console.log("computing count");
            console.log(computing_count);
            console.log("computing connections:");
            console.log(computing_connections.length);
            console.log("computing hosts: ");
            console.log(computing_hosts);
            console.log("computing hash: ");
            console.log(computing_hash);
            */
        });

        worker.on("error", function(err) { console.log(err); });
        worker.on("timeout", function(timeout) { console.log(timeout); });
        worker.on("data", function(data) { console.log("Receive: " + data); });

        worker.on("close", function() {
            var worker_host = worker_addr + ":" + worker_port;
            var index = computing_hash[worker_host];

            if (!(index >= 0)) 
                return;

            delete computing_connections[index];
            delete computing_hosts[index];
            delete computing_hash[worker_host];

            --computing_count;
            if (index != computing_count) {
                computing_connections[index] = computing_connections[computing_count];
                delete computing_connections[computing_count];
                computing_hosts[index] = computing_hosts[computing_count];
                delete computing_hosts[computing_count];
                computing_hash[computing_hosts[computing_count]] = index;
            }

            /*
            console.log("Connection closed. ");
            console.log(worker_host);
            console.log("computing count");
            console.log(computing_count);
            console.log("computing connections:");
            console.log(computing_connections.length);
            console.log("computing hosts: ");
            console.log(computing_hosts);
            console.log("computing hash: ");
            console.log(computing_hash);
            */
        });
    }
    
    // new worker with address and port provided
    if ("addr" in query && "port" in query) {
        var worker_host = query["addr"] + ":" + query["port"];

        // new worker 
        if (!(worker_host in computing_hash)) {
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

function new_storage_node(query, response) {

    function create_worker(worker_addr, worker_port) {
        var worker = new net.Socket();

        worker.connect(worker_port, worker_addr, function() {
            var worker_host = worker_addr + ":" + worker_port;
            storage_connections[storage_count] = worker;
            storage_hosts[storage_count] = worker_host;
            storage_hash[worker_host] = storage_count;
            ++storage_count;

            console.log("new connection: ");
            console.log(worker_host);
            console.log("storege count");
            console.log(storage_count);
            console.log("storage_connections:");
            console.log(storage_connections.length);
            console.log("storage_hosts: ");
            console.log(storage_hosts);
            console.log("storage_hash: ");
            console.log(storage_hash);
        });

        worker.on("error", function(err) { console.log(err); });
        worker.on("timeout", function(timeout) { console.log(timeout); });
        worker.on("data", function(data) { console.log("Receive: " + data); });

        worker.on("close", function() {
            var worker_host = worker_addr + ":" + worker_port;
            var index = storage_hash[worker_host];

            if (!(index >= 0)) 
                return;

            delete storage_connections[index];
            delete storage_hosts[index];
            delete storage_hash[worker_host];

            --storage_ount;
            if (index != storage_count) {
                storage_connections[index] = storage_connections[storage_count];
                delete storage_connections[storage_count];
                storage_hosts[index] = storage_hosts[storage_count];
                delete storage_hosts[storage_count];
                storage_hash[storage_hosts[storage_count]] = index;
            }

            console.log("Connection closed. ");
            console.log(worker_host);
            console.log("storage_count");
            console.log(storage_count);
            console.log("storage_connections:");
            console.log(storage_connections.length);
            console.log("storage_hosts: ");
            console.log(storage_hosts);
            console.log("storage_hash: ");
            console.log(storage_ash);
        });
    }
    
    // new worker with address and port provided
    if ("addr" in query && "port" in query) {
        var worker_host = query["addr"] + ":" + query["port"];

        // new worker 
        if (!(worker_host in storage_hash)) {
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

function overview(query, response) {
    response.writeHead(200, { "Content-Type": "text/plain" });
    response.write("Computing nodes: \n");
    for (var key in computing_hash) 
        response.write(computing_hosts[computing_hash[key]] + "\n");
    response.write("\n");
    response.write("Storage nodes: \n");
    for (var key in storage_hash)
        response.write(storage_hosts[storage_hash[key]] + "\n");
    response.end();
}

exports.resources = resources;
exports.new_computing_node = new_computing_node;
exports.new_storage_node = new_storage_node;
exports.overview = overview;
