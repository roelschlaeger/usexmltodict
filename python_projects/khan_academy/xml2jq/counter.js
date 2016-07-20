var addCounters = function() {

    "use strict";

    var CounterFilter = function(name, path, text) {
        var $i = $("<i/>").addClass("fa fa-caret-right");
        var $filter_span = $("<span/>")
            .attr("data-control-type", "button-filter")
            .attr("data-control-action", "filter")
            .attr("data-control-name", name + "-btn")
            .attr("data-path", path)
            .attr("data-selected", "false")
            .text(" " + text);
        $filter_span.prepend($i);
        return $filter_span;
    };

    var CounterCount = function(name, path) {
        var $counter_span = $("<span/>")
            .attr("data-control-type", "counter")
            .attr("data-control-action", "counter")
            .attr("data-control-name", name + "-counter")
            .attr("data-format", "({count})")
            .attr("data-path", path)
            .attr("data-mode", "filter")
            .attr("data-type", "path");
        return $counter_span;
    };

    var Counter = function(name, path, text) {
        return {
            filter: CounterFilter(name, path, text),
            counter: CounterCount(name, path)
        };
    };

    var item1 = Counter("traditional", ".Traditional", "Traditional");
    var item2 = Counter("multicache", ".Multi-cache", "Multi-Cache");
    var item3 = Counter("virtual", ".Virtual", "Virtual");

    var $anchor = $(".jplist-group").children("ul").first();

    $.each([item1, item2, item3], function(n, item) {
        var $li = $("<li/>")
            .append(item.filter)
            .append(item.counter);
        $anchor.append($li);
    });
};
