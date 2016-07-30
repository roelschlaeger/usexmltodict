<!-- http://jplist.com/documentation/js-settings -->

"use strict";

var fillTable = function() {
    var $list = $("#example tbody");

    $list.empty();

    var wpts = data.gpx.wpt;
    wpts.forEach(function(wpt, index) {

        var lat = latstr(wpt["@lat"]);
        var lon = lonstr(wpt["@lon"]);
        var desc = wpt.desc;

        var short = wpt.extensions["groundspeak:cache"]["groundspeak:short_description"]
        var short_text = short["#text"];
        if (short["@html"] === "True") {
            short_text = $("<div/>").html(short_text).text();
        }

        var long = wpt.extensions["groundspeak:cache"]["groundspeak:long_description"]
        var long_text = long["#text"];
        if (long["@html"] === "True") {
            long_text = $("<div/>").html(long_text).text();
        }

        // if(index === 1) {
        //     console.log(Object.keys(wpt.extensions["groundspeak:cache"]));
        //     console.log(Object.keys(wpt.extensions["gsak:wptExtension"]));
        //     console.log(short["#text"]);
        //     console.log(long["#text"]);
        //     console.log(short_text);
        //     console.log(long_text);
        // }

        var hint = wpt.extensions["groundspeak:cache"]["groundspeak:encoded_hints"]
        var container = wpt.extensions["groundspeak:cache"]["groundspeak:container"]
        var usersort = wpt.extensions["gsak:wptExtension"]["gsak:UserSort"]
        var link = wpt.link;
        var name = wpt.name;
        var sym = wpt.sym;
        //     var time = wpt.time;
        var type = wpt.type.replace("Geocache|", "").replace(" Cache", "");

        // create the <tr> for the row
        var $tr = $("<tr/>")
            .appendTo($list);

        // append <td>s to it for UserSort
        var $td = $("<td/>")
            .appendTo($tr)
            .text(usersort);

        // append short and long descriptions to the name as a popover
        if (!(short_text || long_text)) {
            var $a = $("<span/>").text(name)
        } else {
            var $a = $("<a/>")
                .attr("href", "#")
                .attr("data-toggle", "popover")
                .attr("data-trigger", "focus")
                .attr("data-title", short_text)
                .attr("data-content", long_text)
                // .attr("text-decoration", "underline")
                .text(name);
        }

        $td = $("<td/>")
            .append($a)
            .appendTo($tr);

        if (link["@href"]) {
            // var tlink = link["@href"];
            var tlink = link["@href"].replace("cache_details", "cdpf") + "&lc=10";
            var descplus = $("<a/>")
                .attr("href", tlink)
                .attr("target", "_blank")
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

    $('[data-toggle="popover"]').popover();
};
