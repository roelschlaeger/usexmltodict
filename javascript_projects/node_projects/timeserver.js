// javascript template
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

// Created:       Fri 15 Nov 2013 04:06:30 PM CST
// Last Modified: Fri 15 Nov 2013 04:50:17 PM CST

var net = require('net')

function zf(s) {
    if (s<10) s = "0" + s;
    return s;
};

var server = net.createServer(function (socket) {
    // socket handling logic
    var date = new Date();

    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    var hour = date.getHours();
    var minute = date.getMinutes();

//  if (month < 10) month = "0" + month;
//  if (day < 10) day = "0" + day;
//  if (hour < 10) hour = "0" + hour;
//  if (minute < 10) minute = "0" + minute;

    var data = year + "-" + zf(month) + "-" + zf(day) + " " + zf(hour) + ":" + zf(minute) + "\n";
    socket.write(data);
    socket.end();
});

server.listen(8000)
