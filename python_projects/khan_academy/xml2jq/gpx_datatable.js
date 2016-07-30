<!-- http://jplist.com/documentation/js-settings -->

"use strict";

var fillTable = function() {
    var $list = $("#example tbody");

    $list.empty();

    var wpts = data.gpx.wpt;
    wpts.forEach(function(wpt, index) {


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

        var archived = wpt.extensions["groundspeak:cache"]["@archived"]
        var available = wpt.extensions["groundspeak:cache"]["@available"]
        var container = wpt.extensions["groundspeak:cache"]["groundspeak:container"]
        var desc = wpt.desc;
        var hint = wpt.extensions["groundspeak:cache"]["groundspeak:encoded_hints"]
        var lat = latstr(wpt["@lat"]);
        var link = wpt.link;
        var lon = lonstr(wpt["@lon"]);
        var name = wpt.name;
        var sym = wpt.sym;
        var type = wpt.type.replace("Geocache|", "").replace(" Cache", "");
        var usersort = wpt.extensions["gsak:wptExtension"]["gsak:UserSort"]
        //     var time = wpt.time;

        // add a row to the table
        var $tr = $("<tr/>")
            .appendTo($list);

        // append <td>s to it for UserSort
        var $td = $("<td/>")
            .appendTo($tr)
            .text(usersort);

        // append name
        $td = $("<td/>")
            .appendTo($tr)
            .html(name);

        if (short_text || long_text) {
            // append short description to the usersort as a popover
            var $shorttext = $("<a/>")
                .attr("href", "#")
                .attr("data-toggle", "popover")
                .attr("data-trigger", "focus")
                .attr("data-title", short_text)
                .attr("data-content", long_text)
                .appendTo($td)
                .html("<p style='font-size: 80%; font-style: normal'>Descriptions</p>");
        }

        // add a link to the printer-format of the cache description page
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

        // special annotation if the cache is archived
        if (!(archived === "False")) {
            $tr.addClass("archived");
        }

        // special annotation if the cache is unavailable
        if (!(available === "True")) {
            $td.addClass("unavailable");
        }

        $td = $("<td/>")
            .appendTo($tr)
            .html(type + "<br />" + container);

//      $td = $("<td/>")
//          .appendTo($tr)
//          .text(container);

        $td = $("<td/>")
            .appendTo($tr)
            .text(hint);

        $td = $("<td/>")
            .appendTo($tr)
            .html(lat + "<br />" + lon);
    });

    // now initialize all of the popovers
    $('[data-toggle="popover"]').popover();
};
