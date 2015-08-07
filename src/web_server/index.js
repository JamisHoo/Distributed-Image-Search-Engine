#!/usr/bin/env node
/******************************************************************************
 *  Copyright (c) 2015 Jamis Hoo
 *  Distributed under the MIT license 
 *  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 *  
 *  Project: Distributed Image Search Engine
 *  Filename: index.js
 *  Version: 1.0
 *  Author: Jamis Hoo
 *  E-mail: hoojamis@gmail.com
 *  Date: Aug  7, 2015
 *  Time: 21:49:31
 *  Description: master server
 *****************************************************************************/

var express = require("express");
var fs = require("fs");
var net = require("net");
var _ = require("underscore");


var app = express();

// home page
var search_html = fs.readFileSync("public/index.html").toString();

// connections with computing nodes
var computing_node_count = 0;
var computing_hosts = [ ];
var computing_hosts_hash = { };


// connections with storage nodes
var storage_node_count = 0;
var storage_hosts = [];
var storage_hosts_hash = { };


// root redirect to index.html
app.get("/", function(req, res) {
    console.log("get /");
    res.redirect("/index.html");
});

// index.html 
app.get("/index.html", function(req, res) {
    console.log("get /index.html");
    var rand1 = computing_hosts[Math.floor(Math.random() * computing_node_count)];
    var rands = _.sample(storage_hosts, 20).join();

    var content = 
        search_html.replace("COMPUTING_NODE_HOST", rand1)
                   .replace("STORAGE_NODE_HOST", rands);
    
    res.send(content);
});

// accept new computing node
app.get("/new_computing_node", function(req, res) {
    function create_connection(addr, http_port, tcp_port) {
        var host = addr + ":" + http_port;
        var sock = new net.Socket();

        sock.connect(tcp_port, addr, function() {
            computing_hosts[computing_node_count] = host;
            computing_hosts_hash[host] = computing_node_count;
            ++computing_node_count;

            console.log(computing_node_count); console.log(computing_hosts); console.log(computing_hosts_hash);
        });
        
        sock.on("close", function() {
            index = computing_hosts_hash[host];

            if (!(index >= 0)) 
                return;

            delete computing_hosts[index];
            delete computing_hosts_hash[host];
            --computing_node_count;

            if (index != computing_node_count) {
                computing_hosts[index] = computing_hosts[computing_node_count];
                computing_hosts_hash[computing_hosts[computing_node_count]] = index;
                delete computing_hosts[computing_node_count];
                delete computing_hosts_hash[host];
            }

            console.log(computing_node_count); console.log(computing_hosts); console.log(computing_hosts_hash);
        });

        sock.on("error", function(error) { console.log(error); });
        // TODO timeout callback arguments?
        sock.on("timeout", function(timeout) { console.log(timeout); });
        sock.on("data", function(data) { console.log(data); });
    }


    if ("addr" in req.query && "http_port" in req.query && "tcp_port" in req.query) {
        var host = req.query.addr + ":" + req.query.http_port;
        if (!(host in computing_hosts_hash)) {
            create_connection(req.query.addr, req.query.http_port, req.query.tcp_port);
            res.send("Try to connect to " + host + ". ");
        } else {
            res.send(host + " already in computing hosts list. ");
        }
    } else {
        res.send("Address or port of computing node isn't provided. ");
    } 
});

// accept new storage node
app.get("/new_storage_node", function(req, res) {
    function create_connection(addr, http_port, tcp_port) {
        var host = addr + ":" + http_port;
        var sock = new net.Socket();

        sock.connect(tcp_port, addr, function() {
            storage_hosts[storage_node_count] = host;
            storage_hosts_hash[host] = storage_node_count;
            ++storage_node_count;

            console.log(storage_node_count); console.log(storage_hosts); console.log(storage_hosts_hash);
        });
        
        sock.on("close", function() {
            index = storage_hosts_hash[host];

            if (!(index >= 0)) 
                return;

            delete storage_hosts[index];
            delete storage_hosts_hash[host];
            --storage_node_count;

            if (index != storage_node_count) {
                storage_hosts[index] = storage_hosts[storage_node_count];
                storage_hosts_hash[storage_hosts[storage_node_count]] = index;
                delete storage_hosts[storage_node_count];
                delete storage_hosts_hash[host];
            }

            console.log(storage_node_count); console.log(storage_hosts); console.log(storage_hosts_hash);
        });

        sock.on("error", function(error) { console.log(error); });
        // TODO timeout callback arguments?
        sock.on("timeout", function(timeout) { console.log(timeout); });
        sock.on("data", function(data) { console.log(data); });
    }


    if ("addr" in req.query && "http_port" in req.query && "tcp_port" in req.query) {
        var host = req.query.addr + ":" + req.query.http_port;
        if (!(host in storage_hosts_hash)) {
            create_connection(req.query.addr, req.query.http_port, req.query.tcp_port);
            res.send("Try to connect to " + host + ". ");
        } else {
            res.send(host + " already in storage hosts list. ");
        }
    } else {
        res.send("Address or port of computing node isn't provided. ");
    } 
});

// overview
app.get("/overview", function(req, res) {
    var content = "Computing nodes: \n";
    for (var key in computing_hosts_hash)
        content += computing_hosts[computing_hosts_hash[key]] + "\n";
    content += "\n";

    content += "Storage nodes: \n";
    for (var key in storage_hosts_hash)
        content += storage_hosts[storage_hosts_hash[key]] + "\n";
    content += "\n";

    res.set('Content-Type', 'text/plain');
    res.send(content);
});


// search at public dir
app.use(express.static("public"));

// 404
app.use(function(req, res, next) {
    res.status(404).send('<h1>404 Not Found</h1>');
});

var server = app.listen(3000, function () {
    var host = server.address().address;
    var port = server.address().port;

    console.log('DISE web server listening at http://%s:%s', host, port);
});
