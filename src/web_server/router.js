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
 *  Description: 
 *****************************************************************************/


function route(handle, pathname, query, response) {
    // find function to handle 
    if (typeof handle[pathname] === 'function') {
        handle[pathname](query, response);
    // if no function handle this path
    } else {
        // 404
        response.writeHead(404, { "Content-Type": "text/plain"} );
        response.write("404 Not found. ");
        response.end();
    }
}

exports.route = route;
