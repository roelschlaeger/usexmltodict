// javascript template
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

// Created:       Fri 15 Nov 2013 04:06:30 PM CST
// Last Modified: Fri 15 Nov 2013 04:42:54 PM CST

var net = require('net')

var server = net.createServer(function (socket) {
    // socket handling logic
    var date = new Date();

    var year = date.getFullYear();
    var month = date.getMonth() + 1;
    var day = date.getDate();
    var hour = date.getHours();
    var minute = date.getMinutes();

    if (month < 10) month = "0" + month;
    if (day < 10) day = "0" + day;
    if (hour < 10) hour = "0" + hour;
    if (minute < 10) minute = "0" + minute;
    var data = year + "-" + month + "-" + day + " " + hour + ":" + minute;
    socket.end(data);
})

server.listen(8000)
