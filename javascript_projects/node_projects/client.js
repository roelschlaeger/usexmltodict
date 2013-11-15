// javascript template
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

// Created:       Fri 15 Nov 2013 11:42:36 AM CST
// Last Modified: Fri 15 Nov 2013 12:19:16 PM CST

http = require('http');

arg = process.argv[2];
console.log('arg =', arg);

http.get(arg, function(res) {
    res.setEncoding('utf8');
    console.log('Got response: ', res);
    res
}
).on('data', function(data) {
    console.log('data=', data);
}
).on('error', function(err) {
    console.log('error =', err);
});
