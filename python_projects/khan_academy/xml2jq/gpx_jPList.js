<!-- http://jplist.com/documentation/js-settings -->

var fillListDiv = function() {
    var $list = $(".list");
    $list.empty();


    var wpts = data.gpx.wpt;
    wpts.forEach(function(wpt, index) {
        $item = $("<div/>")
            .addClass("list-item box")
            .appendTo($list);

        $table = $("<table/>")
            .append("<caption/>")
            .append("<thead/>")
            .append("<tbody/>")
            .appendTo($item);

        $thead = $table.find("thead");
        // console.log($thead);
        $row = $("<tr/>").appendTo($thead);
        keys = ["lat", "lon", "desc", "name", "sym", "time", "type"];
        keys.forEach(
            function(element) {
                $row.append($("<th/>").text(element));
            });

        // console.log(wpt);
        var $row = $("<tr/>").appendTo($table);

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
            var td = $("<td/>").addClass(name).text(property);
            $row.append(td);
        });

        $item.append($("<br/>"));
    });
};
