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

        var available = wpt.extensions["groundspeak:cache"]["@available"]
        var archived = wpt.extensions["groundspeak:cache"]["@archived"]

        console.log(available);

        if (index === 1) {
            console.log(Object.keys(wpt.extensions["groundspeak:cache"]));
            // console.log(Object.keys(wpt.extensions["gsak:wptExtension"]));
            // console.log(short["#text"]);
            //     console.log(long["#text"]);
            //     console.log(short_text);
            //     console.log(long_text);
        }

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
        var $a1 = "";
        var $a2 = "";

        if (short_text) {
            $a1 = $("<a/>")
                .attr("href", "#")
                .attr("data-toggle", "popover")
                .attr("data-trigger", "focus")
                .attr("data-title", "Short Description")
                .attr("data-content", short_text)
                .html("&nbsp;S");
        }

        if (long_text) {
            $a2 = $("<a/>")
                .attr("href", "#")
                .attr("data-toggle", "popover")
                .attr("data-trigger", "focus")
                .attr("data-title", "Long Description")
                .attr("data-content", long_text)
                .html("&nbsp;L");
        }

        // var $a = $("<span/>").text(name)
        $td = $("<td/>")
            .text(name)
            .append($a1)
            .append($a2)
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

        if (!(archived === "False")) {
            $tr.addClass("archived");
        }

        if (!(available === "True")) {
            $td.addClass("unavailable");
        }

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
