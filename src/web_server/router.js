/******************************************************************************
 *  Copyright (c) 2015 Jamis Hoo
 *  Distributed under the MIT license 
 *  (See accompanying file LICENSE or copy at http://opensource.org/licenses/MIT)
 *  
 *  Project:
 *  Filename: router.js
 *  Version: 1.0
 *  Author: Jamis Hoo
 *  E-mail: hjm211324@gmail.com
 *  Date: Jul 31, 2015
 *  Time: 23:56:29
 *  Description: route requests
 *****************************************************************************/


function route(handle, pathname, query, response) {
    // access static resources
    if (pathname.indexOf("/static/") == 0) {
        handle["/static"](pathname, response); 
    // find function to handle 
    } else if (typeof handle[pathname] === 'function') {
        handle[pathname](query, response);
    // if no function handle this path
    } else {
        // 404
        response.writeHead(404, { "Content-Type": "text/html"} );
        response.write("<h1>404 Not Found</h1>");
        response.end();
    }
}

exports.route = route;
