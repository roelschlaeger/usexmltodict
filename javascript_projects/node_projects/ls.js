// ls.js
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap
//
// Created:       TIMESTAMP
// Last Modified: TIMESTAMP

var fs = require("fs");
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
