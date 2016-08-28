// Document Ready function
$(document).ready(function() {

    var Data = function(data) {
        var self = this;

        this.metadata = data.gpx.metadata;
        // console.log(this.metadata);

        this.h1 = this.metadata.desc;
        this.h2 = this.metadata.time;
        var bounds = this.metadata.bounds;
        var minlat = bounds["@minlat"];
        var maxlat = bounds["@maxlat"];
        var minlon = bounds["@minlon"];
        var maxlon = bounds["@maxlon"];
        this.minlat = "Minlat: " + latstr(minlat);
        this.maxlat = "Maxlat: " + latstr(maxlat);
        this.minlon = "Minlon: " + lonstr(minlon);
        this.maxlon = "Maxlon: " + lonstr(maxlon);
        this.caption = [
            this.minlat,
            this.maxlat,
            this.minlon,
            this.maxlon,
        ].join(", ");

        // self.ContextMenuClick = function(event) { console.log(event); };

        self.GeocacheList = CreateGeocacheList(data.gpx.wpt);

        self.thList = [
            "index",
            "name",
            "link",
            "type",
            "container",
            "encoded_hints",
            "latitude",
            "longitude",
            "Logs"
        ];

        // self.synthesized_name = function(wpt) {
        //     return [
        //         wpt.sym,
        //         wpt.name,
        //         wpt.desc
        //     ].join("/");
        // };

        self.logsButtonClick = function(data) {
            var logs = data.cache_object_logs;
            // console.log(logs);
            var j = JSON.stringify(logs, null, 2);
            console.log(j);
            var ologs = logs["groundspeak:log"];
            // console.log(ologs);
            var result = []
            for (var i = 0; i < ologs.length; i++) {
                var log = ologs[i];
                // console.log(log);

                var log_id = log["@id"];
                var log_date = log["groundspeak:date"];
                var log_finder = log["groundspeak:finder"];
                var log_text = log["groundspeak:text"]
                var log_type = log["groundspeak:type"]

                var log_finder_id = log_finder["@id"];
                var log_finder_text = log_finder["#text"];

                // console.log(log_text);
                var log_text_text = log_text["#text"];
                var log_text_encoded = log_text["@encoded"];

                // console.log(i);
                result_string = [
                    i,
                    log_date,
                    log_id,
                    log_type,
                    log_finder_id,
                    log_finder_text,
                    log_text_encoded,
                    log_text_text
                ].join("\n");
                result.push(result_string)
            }
            alert(result.join("\n---- Note ----\n"));
        };

        self.logsButtonName = function(data) {
            var logs = data.cache_object_logs;
            var ologs = logs["groundspeak:log"];
            return ologs.length + " Logs";
        }

    };

    myData = new Data(data);

    ko.applyBindings(myData);
})
