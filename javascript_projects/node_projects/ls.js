// ls.js
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

// Created:       Fri 15 Nov 2013 12:50:16 PM CST
// Last Modified: Fri 15 Nov 2013 12:50:55 PM CST

var fs = require("fs");
if (process.argv.length <= 3) console.error("Too few arguments");
var regex = new RegExp( "\\." + process.argv[3] + "$");
var filelist = fs.readdir(
        process.argv[2], 
        function(err, list) {
            if (err) throw err;
            for (var i=0; i<list.length; i++) {
                var fn = list[i];
                if (regex.test(fn)) {
                    console.log(fn);
                }
            }
        });
