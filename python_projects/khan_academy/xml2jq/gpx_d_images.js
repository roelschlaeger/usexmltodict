<!-- http://jplist.com/documentation/js-settings -->
<!-- http://www.w3schools.com/jquerymobile/jquerymobile_pages.asp -->

"use strict";

var MAX_FINDS_LENGTH = 20; // number of Find characters in the Find string
var MAX_LOGS_PER_DIALOG = 30; // use -1 for "all"
var MAX_ROUTE_POINTS = -1; // number of main table elements; use -1 for "all"

var make_logs_table = function(logs) {
    var $table = $('<table/>')
        .attr("alt", "Logs table")
        .addClass("logs")
        .addClass("table table-striped table-bordered");

    // DataTable requires <thead> and <tbody>
    var $thead = $("<thead/>").appendTo($table);
    var $tbody = $("<tbody/>").appendTo($table);

    // create the header row
    var $tr = $('<tr/>').appendTo($thead);

    $.each(
        [
            "date",
            "type",
            "finder",
            "text"
        ],
        function(n, e) {
            $("<th/>")
                .appendTo($tr)
                .text(e);
        });

    // create the body rows
    $.each(logs, function(n, e) {
        if ((MAX_LOGS_PER_DIALOG !== -1) && (n >= MAX_LOGS_PER_DIALOG)) {
            return false;
        }

        // var id = e["@id"];
        var date = e["groundspeak:date"];
        var type = e["groundspeak:type"];
        var _finder = e["groundspeak:finder"];
        var _text = e["groundspeak:text"];

        var finder = "UNKNOWN"
        if (_finder) {
            finder = _finder["#text"];
        }

        // var text = "NO TEXT";
        var text = "NO TEXT";
        if (_text) {
            // if (_text["@encoded"] !== "False") {
            text = _text["#text"]
                // }
        }

        var $tr = $('<tr>').appendTo($tbody);
        var td = $("<td/>").appendTo($tr).text(date);
        var td = $("<td/>").appendTo($tr).text(type);
        var td = $("<td/>").appendTo($tr).text(finder);
        var td = $("<td/>").appendTo($tr).text(text);
    });
    return $table;
};

var fillImgTable = function() {
    var $list = $("#images tbody");

    $list.empty();
    $("#pagetwo").remove();

    var wpts = data.gpx.wpt;
    wpts.forEach(function(wpt, index) {

        if (
            (MAX_ROUTE_POINTS !== -1) &&
            (index >= MAX_ROUTE_POINTS)
        ) {
            return false;
        }

        var usersort = wpt.extensions["gsak:wptExtension"]["gsak:UserSort"]
        var name = wpt.name;
        var desc = wpt.desc;
        var cache = wpt.extensions["groundspeak:cache"]
        var logs = cache["groundspeak:logs"] || {
            "groundspeak:log": []
        };
        logs = logs["groundspeak:log"];

        var page_link = "log_" + name;
        var inner_page_link = "inner_" + page_link;
        var $new_table = make_logs_table(logs);

        var $new_table_div = $("<div/>")
            .addClass("new_table_div")
            .attr("id", inner_page_link)
            .append($("<hr style='border-color: red; border-width: 3px;'>"))
            .append($("<h1/>").text(desc))
            .append($new_table)
            .append($("<a href='#pageone'>Go to Page One</a>"));

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

        // append description
        $td = $("<td/>")
            .appendTo($tr)
            .html(desc);

        // append logs information
        $td = $("<td/>")
            .appendTo($tr)
            .html(logs.length + "&nbsp;" + finds + " ");

        if (logs.length) {
            // compute link name
            var $a = $("<a/>")
                .attr("href", "#" + page_link)
                .html("<br />Logs " + name)
                .appendTo($td);

            var $new_main = $("<div/>")
                .attr("data-role", "main")
                .addClass("ui-content")
                .append($new_table_div);

            var $new_page = $("<div/>")
                .attr("data_role", "page")
                .attr("data-dialog", "true")
                .attr("id", page_link)
                .append($new_main);

            $("#pageone")
                .append($new_page);
        }

    });

};
