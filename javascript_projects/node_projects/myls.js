// myls.js
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

// Created:       Thu 14 Nov 2013 04:26:59 PM CST
// Last Modified: Fri 15 Nov 2013 10:35:07 AM CST

module.exports = function listdir (dirname, extension, callback) {

    var fs = require("fs");

    // create the regex just once
    // add extension prefix if needed
//  extension = extension.replace(/^\\./g, ".");
//  console.log(extension);

    if (extension[0] !== ".") extension = "\\." + extension;
    // add end-of-string marker if needed
    if (extension[extension.length-1] !== "$") extension += "$"
    var regex = new RegExp(extension);

    var output_list;

    fs.readdir(
            dirname, 
            function(err, fileList) {
                output_list = [];
                if (err) return callback(err);
                for (var i=0; i<fileList.length; i++) {
                    var fn = fileList[i];
                    if (regex.test(fn)) {
                        output_list.push(fn);
                    }
                }
                callback(null, output_list);
            });
};
