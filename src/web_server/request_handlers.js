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
 *  Description: 
 *****************************************************************************/


var net = require("net")


var tcp_count = 0;
var tcp_connections = []
var tcp_hosts = []
var tcp_hash = {}

var query_counter = 0;
var query_hash = {}

function root(query, response) {
    response.writeHead(200, { "Content-Type": "text/plain" });
    response.write("Hello I'm root. ");
    response.end();
}

function search(query) {
    // no worker is working
    if (tcp_count == 0) {
        response.writeHead(503, { "Content-Type": "text/plain" });
        response.write("No worker is working. ");
        response.end();
    }
    
    // keywords non-empty
    if ("keywords" in query) {
        // extract keywords
        var keywords = query["keywords"].replace(/\s/g, '');
        
        // if keywords only consists of whitespaces
        if (keywords.replace(/+/g, '').length == 0)
            break; 

        // send query to worker
        rand = Math.floor(Math.random() * tcp_count);
        worker = tcp_connections[rand];
        worker.write(query_counter + ":" + keywords + "\n", "UTF8");
        
        query_hash[query_counter] = response;
        ++query_counter;
    }
    
    // keywords empty
    response.writeHead(200, { "Content-Type": "text/plain" });
    response.write("Hello I'm search. ");
    response.end();
}

function newworker(query) {

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

        });

        worker.on("close", function() {
            var worker_host = worker_addr + ":" + worker_port;
            var index = tcp_hash[worker_host];
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
exports.search = search;
exports.newworker = newworker;

