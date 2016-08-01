<!-- http://jplist.com/documentation/js-settings -->

"use strict";

var make_logs_table = function(logs) {
    var $table = $('<table/>').addClass("logs");

    var $thead = $("<thead/>").appendTo($table);
    var $tbody = $("<tbody/>").appendTo($table);

    var $tr = $('<tr/>').appendTo($thead);

    $.each(
        ["id", "date", "type", "finder", "text"], 
        function(n, e) {
            $("<th/>")
                .appendTo($tr)
                .text(e);
    });

    $.each(logs, function(n, e) {
        var id = e["@id"];
        var date = e["groundspeak:date"];
        var type = e["groundspeak:type"];
        var _finder = e["groundspeak:finder"];
        var _text = e["groundspeak:text"];
        var finder = "UNKNOWN"
        if (_finder) {
            finder = _finder["#text"];
        }
        var text = "NO TEXT";
        if (_text) {
            if (_text["@encoded"] !== "False"){
            }
            var text = _text["#text"]
        }
//      if (n === 0) {
//          console.log(_finder);
//          console.log(_text);
//      }
        var $tr = $('<tr>').appendTo($tbody);
        var td = $("<td/>").appendTo($tr).text(id);
        var td = $("<td/>").appendTo($tr).text(date);
        var td = $("<td/>").appendTo($tr).text(type);
        var td = $("<td/>").appendTo($tr).text(finder);
        var td = $("<td/>").appendTo($tr).text(text);
    });
    return $table;
};

var MAX_FINDS_LENGTH = 20;

var fillImgTable = function() {
    var $list = $("#images tbody");

    $list.empty();

    var wpts = data.gpx.wpt;
    wpts.forEach(function(wpt, index) {

        var usersort = wpt.extensions["gsak:wptExtension"]["gsak:UserSort"]
        var name = wpt.name;
        var desc = wpt.desc;
        var cache = wpt.extensions["groundspeak:cache"]
        var logs = cache["groundspeak:logs"] || { "groundspeak:log": [] };
        logs = logs["groundspeak:log"];
        var $new_table = make_logs_table(logs);

        var finds = "";
        $.each(logs, function(n, e) {
            var find_type = e["groundspeak:type"];
            if (find_type) {
                finds += e["groundspeak:type"][0];
            }
        });
        if (finds.length > MAX_FINDS_LENGTH) {
            finds = finds.substr(0, MAX_FINDS_LENGTH) + "..."
        }

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

        $td = $("<td/>")
            .appendTo($tr)
            .html(desc);

        $td = $("<td/>")
            .appendTo($tr)
            .html(logs.length + " " + finds);

        var $a = $("<span/>")
            .attr("href", "#")
            .attr("rel", "_blank")
            .html($new_table);
        $td.append($a);

//      $td = $("<td/>")
//          .appendTo($tr)
//          .html(finds);

    });

};
