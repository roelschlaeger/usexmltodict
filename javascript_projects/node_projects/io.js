// read file system
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

var fs = require("fs");

var buffer;
var count = 0;

if (process.argv.length <= 2) {

    console.log("No filename provided");

} else {

    var filename = process.argv[2];

    buffer = fs.readFileSync(filename);

    count = 0;
    for (var i=0; i<buffer.length; i++) {
        var ch = buffer[i];
        if (ch === 10) {
            count++;
        }
    }

    console.log(count)
}

