<!-- http://jplist.com/documentation/js-settings -->

"use strict";

var fillListDiv = function() {
    var $list = $(".row .panel .table tbody");
    console.log($list);
    $list.empty();

    var wpts = data.gpx.wpt;
    wpts.forEach(function(wpt, index) {

        //     var $item = $("<div/>")
        //         .addClass("list-item")
        //         .addClass("box")
        //         .addClass("right")
        //         .appendTo($list);
        //
        //     var $div = $("<div/>")
        //         .addClass("block right")
        //         .appendTo($item);
        //
        var lat = latstr(wpt["@lat"]);
        var lon = lonstr(wpt["@lon"]);
        var desc = wpt.desc;
        // var extensions = wpt.extensions;
        var usersort = wpt.extensions["gsak:wptExtension"]["gsak:UserSort"]
        // console.log(usersort);
        // console.log(extensions["gsak:wptExtension"]);
        var link = wpt.link;
        var name = wpt.name;
        var sym = wpt.sym;
        //     var time = wpt.time;
        var type = wpt.type.replace("Geocache|", "").replace(" Cache", "");
        //     var text = {
        //         "index": index,
        //         "name": name,
        //         "desc": desc,
        //         "lat": latstr(lat),
        //         "lon": lonstr(lon),
        //         // "extensions": extensions,
        //         // "link": link,
        //         "date": time,
        //         "sym": sym,
        //         "type": type,
        //     };
        //
        //     $.each(text, function(name, property){
        //         var td = $("<span/>")
        //             .addClass(name)
        //             .addClass("bob")
        //             .text(property);
        //         if (name === "name" ) {
        //             td.addClass("title");
        //         } else if (name === "sym" || name === "type") {
        //             td.addClass(property);
        //         }
        //         $div.append(td);
        //     });
        var $tr = $("<tr/>")
            .appendTo($list);
        var $td;

        $td = $("<td/>")
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
            .html(lat + "&nbsp;" + lon);

        $td = $("<td/>")
            .appendTo($tr)
            .text(type);

    });
};
