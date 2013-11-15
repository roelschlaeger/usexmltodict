// javascript template
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

// Created:       Fri 15 Nov 2013 11:42:36 AM CST
// Last Modified: Fri 15 Nov 2013 01:28:34 PM CST

http = require('http');

var done = 0;

function one(arg, result) {
    var str = '';
    console.log("get: ", arg);
    http.get(arg, function(res) {
        res.setEncoding('utf8');
        res.on('data', function(chunk) {str += chunk});
        res.on('end', function() {result = str; done += 1});
        res.on('error', console.error);
    });
};

arg1 = process.argv[2];
console.log("arg1=", arg1);

arg2 = process.argv[3];
console.log("arg2=", arg2);

arg3 = process.argv[4];
console.log("arg3=", arg3);

var v1, v2, v3;
one(arg1, v1);
one(arg2, v2);
one(arg3, v3);

console.log(done);
while (done < 1);
console.log(done);
while (done < 2);
console.log(done);
while (done < 3);
console.log(done);

console.log(v1);
console.log(v2);
console.log(v3);

