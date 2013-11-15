// javascript template
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

// Created:       Thu 14 Nov 2013 04:19:22 PM CST
// Last Modified: Fri 15 Nov 2013 10:34:09 AM CST

var listdir = require("./myls.js");

var list;

if (process.argv.length <= 3) throw "Too few arguments";

listdir(process.argv[2], process.argv[3], function(err, list) {
    if (err) {
        console.log(err);
    } else {
        for (var i=0; i<list.length; i++) {
            console.log(list[i]);
        }
    }
});

