<!-- http://jplist.com/documentation/js-settings -->

var fillListDiv = function() {
    var $list = $(".list");
    // $list.empty();


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
            "lat": lat,
            "lon": lon,
            "desc": desc,
            // "extensions": extensions,
            // "link": link,
            "name": name,
            "sym": sym,
            "time": time,
            "type": type,
        };

        $.each(text, function(name, property){
            var td = $("<p/>").addClass(name).text(property);
            $item.append(td);
        });
    });
};
