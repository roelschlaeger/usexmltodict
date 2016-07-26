<!-- http://jplist.com/documentation/js-settings -->

"use strict";

var fillListDiv = function() {
    var $table = $("<table/>")
        .addClass("bob")
        .attr("alt", "route table")
        .prependTo($(".list"));

    var $thead = $("<thead/>")
        .appendTo($table);

    var $tfooter = $("<tfooter/>")
        .appendTo($table);

    var $tbody = $("<tbody/>")
        .attr("id", "list")
        .appendTo($table);

    /* create table header */
    var $tr = $("<tr/>")
        .appendTo($thead)

    $.each(
        [
            "index",
            "name",
            "desc",
            "latitude",
            "longitude",
            "time",
            "symbol",
            "type",
        ],
        function(n, e) {
            var $th1 = $("<th/>")
                .text(e)
                .appendTo($tr);
        }
    );

    // var $div = $("<div/>")
    //     .attr("id", "#list");

    /* create table body */
    var wpts = data.gpx.wpt;

    wpts.forEach(function(wpt, index) {

        var $row = $("<tr/>")
            .addClass("list-item")
            .appendTo($tbody);

        var lat = wpt["@lat"];
        var lon = wpt["@lon"];
        var desc = wpt.desc;
        // var extensions = wpt.extensions;
        // var link = wpt.link;
        var name = wpt.name;
        var sym = wpt.sym;
        var time = wpt.time;
        var type = wpt.type;
        var text = {
            "index": index,
            "name": name,
            "desc": desc,
            "lat": latstr(lat),
            "lon": lonstr(lon),
            // "extensions": extensions,
            // "link": link,
            "date": time,
            "sym": sym,
            "type": type.replace("Geocache|", "").replace(" Cache", ""),
        };

        $.each(text, function(name, property) {
            var td = $("<td/>")
                .addClass(name)
                .text(property);
            if (name === "name") {
                td.addClass("title");
            } else if (name === "sym" || name === "type") {
                td.addClass(property);
            }
            $row.append(td);
        });

    });

};
