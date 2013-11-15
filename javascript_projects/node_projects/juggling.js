// javascript template
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

// Created:       Fri 15 Nov 2013 11:42:36 AM CST
// Last Modified: Fri 15 Nov 2013 03:42:59 PM CST

http = require('http');

var TIMEOUT = 1000;

var done = 0;
var result = { 
    's1' : '', 
    's2' : '', 
    's3' : ''
};
var arg1 = process.argv[2];
var arg2 = process.argv[3];
var arg3 = process.argv[4];

function callback(res, result_index) {
    var str = '';
//  console.log("starting");
    res.setEncoding('utf8');
    res.on('data', function(chunk) {str += chunk});
    res.on('end', function() {result[result_index] = str; done += 1});
    res.on('error', console.error);
};
        
function one(arg, result) {
    http.get(arg, function(res) {callback(res, result)});
};

// console.log(process.argv);

one(arg1, 's1');
one(arg2, 's2');
one(arg3, 's3');

function checker() {
//  console.log("done=", done);
    if (done === 3) {
//      console.log("Hooray");
        console.log(result['s1']);
        console.log(result['s2']);
        console.log(result['s3']);
    } else {
        setTimeout(checker, TIMEOUT);
    }
}

setTimeout(checker, TIMEOUT);

