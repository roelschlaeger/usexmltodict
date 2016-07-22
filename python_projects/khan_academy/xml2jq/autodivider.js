$(document).ready(function() {

    var divider_value = 0;

    var route_title = data.gpx.metadata.time;

    var $div = $("<div/>")
        .attr("data-role", "page")
        .attr("id", "pagetwo");

    var $div2 = $("<div/>")
        .attr("data-role", "main")
        .addClass("ui-content")
        .appendTo($div);

    var $h2 = $("<h2/>")
        .appendTo($div2)
        .text(route_title);

    var $ul = $("<ul/>")
        .attr("data-role", "listview")
        .attr("data-inset", "true")
        .appendTo($div2);

    var wpts = data.gpx.wpt;

    $(wpts).each(function(n, e) {
        var extensions = e.extensions;
        var wptExtension = extensions["gsak:wptExtension"];
        var cache = extensions["groundspeak:cache"];
        var usersort = wptExtension["gsak:UserSort"];

        var index = Math.ceil((parseInt(usersort) / 100)) * 100;
        if (index !== divider_value) {
            divider_value = index;
            $li = $("<li/>")
                .attr("data-role", "list-divider")
                .appendTo($ul)
                .text(index);
        }

        var desc = e.desc;
        var name = usersort + " " + desc;
        var $li = $("<li/>")
            .appendTo($ul);

        var $a = $("<a/>")
            .attr("href", "#")
            .appendTo($li)
            .text(name);

        // console.log($li);
    })
    $("body").append($div);
});
