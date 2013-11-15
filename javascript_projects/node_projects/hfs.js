// javascript template
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

// Created:       Fri 15 Nov 2013 04:57:17 PM CST
// Last Modified: Fri 15 Nov 2013 05:38:13 PM CST

// HTTP File Streamer

http = require('http');
fs = require('fs');

http.createServer( function(request, response) {
    fs.createReadStream(process.argv[2]).pipe(response);
}).listen(8000);
