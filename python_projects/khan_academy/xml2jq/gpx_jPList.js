<!-- http://jplist.com/documentation/js-settings -->

var fillListDiv = function() {
    var $list = $(".list");
    $list.empty();


    var wpts = data.gpx.wpt;
    wpts.forEach(function(wpt, index) {
        $item = $("<div/>")
            .addClass("list-item")
            .appendTo($list);

        var lat = wpt["@lat"];
        var lon = wpt["@lon"];
        var desc = wpt.desc;
        // var extensions = wpt.extensions;
        // var link = wpt.link;
        var name = wpt.name;
        var sym = wpt.sym;
        // console.log(sym);
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
            "time": time,
            "sym": sym,
            "type": type.replace("Geocache|", "").replace(" Cache", ""),
        };

        $.each(text, function(name, property){
            var td = $("<span/>")
//              .attr("style", "font-family: monospace; border: solid black 1px; padding: 3px; margin: 1px;")
                .addClass("bob")
                .addClass("architecture")
//              .addClass("christmas")
//              .addClass("nature")
//              .addClass("lifestyle")
                .addClass(name)
                .text(property);
            $item.append(td);
        });
    });
};
