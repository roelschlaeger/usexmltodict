// javascript template
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

// Created:       Fri 15 Nov 2013 11:42:36 AM CST
// Last Modified: Fri 15 Nov 2013 12:54:07 PM CST

http = require('http');

http.get(process.argv[2], function(res) {
    var str = '';
    res.setEncoding('utf8');
    res.on('data', function(chunk) {str += chunk});
    res.on('error', console.error);
    res.on('end', function() {
        console.log(str.length);
        console.log(str);
    });
});

