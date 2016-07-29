<!-- http://jplist.com/documentation/js-settings -->

"use strict";

var fillListDiv = function() {
    var $list = $(".row .panel .table tbody");

    // $list.empty();

    var wpts = data.gpx.wpt;
    wpts.forEach(function(wpt, index) {

        var lat = latstr(wpt["@lat"]);
        var lon = lonstr(wpt["@lon"]);
        var desc = wpt.desc;
        // var extensions = wpt.extensions;
        console.log(wpt.extensions);
        var hint = wpt.extensions["groundspeak:cache"]["groundspeak:encoded_hints"]
        var container = wpt.extensions["groundspeak:cache"]["groundspeak:container"]
        var usersort = wpt.extensions["gsak:wptExtension"]["gsak:UserSort"]
        var link = wpt.link;
        var name = wpt.name;
        var sym = wpt.sym;
        //     var time = wpt.time;
        var type = wpt.type.replace("Geocache|", "").replace(" Cache", "");

        var $tr = $("<tr/>")
            .appendTo($list);

        var $td = $("<td/>")
            .appendTo($tr)
            .text(usersort);

        $td = $("<td/>")
            .appendTo($tr)
            .text(name);

        if (link["@href"]) {
            var descplus = $("<a/>")
                .attr("href", link["@href"])
                .text(desc);
        } else {
            var descplus = desc;
        }

        $td = $("<td/>")
            .appendTo($tr)
            .html(descplus);

        $td = $("<td/>")
            .appendTo($tr)
            .text(type);

        $td = $("<td/>")
            .appendTo($tr)
            .text(container);

        $td = $("<td/>")
            .appendTo($tr)
            .text(hint);

        $td = $("<td/>")
            .appendTo($tr)
            .html(lat);

        $td = $("<td/>")
            .appendTo($tr)
            .html(lon);

    });
};
