// read file system
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

var fs = require("fs");

var count = 0;

var filename = process.argv[2];

fs.readFile(filename, function(err, data) {
    if (err) throw err;
    count = data.toString().split("\n").length - 1;
    console.log(count)
//  count = 0;
//  for (var i=0; i<data.length; i++) {
//      var ch = data[i];
//      if (ch === 10) {
//          count++;
//      }
//  }
});


