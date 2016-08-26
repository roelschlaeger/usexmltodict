// A Geocache object, incorporating all of the data from the .gpx file,
// generally into a single level
var Geocache = function(wpt) {

    var self = this;

    this.desc = wpt.desc;
    this.lat = latstr(wpt["@lat"]);
    var object_link = wpt.link;
    this.link_text = object_link.text;
    this.link_href = object_link["@href"];
    this.lon = lonstr(wpt["@lon"]);
    this.name = wpt.name;
    this.sym = wpt.sym;
    this.time = wpt["time"];
    this.type = wpt.type.replace("Geocache|", "").replace("Cache", "");

    // extensions
    var extensions = wpt.extensions;
    var cache = extensions["groundspeak:cache"];
    var gsak_wptExtension = extensions["gsak:wptExtension"];

    // cache extension
    this.cache_archived = cache["@archived"];
    this.cache_available = cache["@available"];
    this.cache_container = cache["groundspeak:container"];
    this.cache_country = cache["groundspeak:country"];
    this.cache_difficulty = cache["groundspeak:difficulty"];
    this.cache_encoded_hints = cache["groundspeak:encoded_hints"];
    this.cache_id = cache["@id"];
    this.cache_name = cache["groundspeak:name"];
    this.cache_placed_by = cache["groundspeak:placed_by"];
    this.cache_state = cache["groundspeak:state"];
    this.cache_terrain = cache["groundspeak:terrain"];
    this.cache_type = cache["groundspeak:type"].replace("Cache", "");

    this.cache_object_attributes = cache["groundspeak:attributes"];
    this.cache_object_logs = cache["groundspeak:logs"];
    this.cache_object_long_description = cache["groundspeak:long_description"];
    this.cache_object_owner = cache["groundspeak:owner"];
    this.cache_object_short_description = cache["groundspeak:short_description"];

    // gsak extension
    this.gsak_cacheimages = gsak_wptExtension["gsak:CacheImages"];
    this.gsak_code = gsak_wptExtension["gsak:Code"];
    this.gsak_county = gsak_wptExtension["gsak:County"];
    this.gsak_customdata = gsak_wptExtension["gsak:CustomData"];
    this.gsak_dnf = gsak_wptExtension["gsak:DNF"];
    this.gsak_favpoints = gsak_wptExtension["gsak:FavPoints"];
    this.gsak_firsttofind = gsak_wptExtension["gsak:FirstToFind"];
    this.gsak_gcnote = gsak_wptExtension["gsak:GcNote"];
    this.gsak_guid = gsak_wptExtension["gsak:Guid"];
    this.gsak_ispremium = gsak_wptExtension["gsak:IsPremium"];
    this.gsak_lastgpxdate = gsak_wptExtension["gsak:LastGpxDate"];
    this.gsak_lock = gsak_wptExtension["gsak:Lock"];
    this.gsak_resolution = gsak_wptExtension["gsak:Resolution"];
    this.gsak_smartname = gsak_wptExtension["gsak:SmartName"];
    this.gsak_user2 = gsak_wptExtension["gsak:User2"];
    this.gsak_user3 = gsak_wptExtension["gsak:User3"];
    this.gsak_user4 = gsak_wptExtension["gsak:User4"];
    this.gsak_userdata = gsak_wptExtension["gsak:UserData"];
    this.gsak_userflag = gsak_wptExtension["gsak:UserFlag"];
    this.gsak_usersort = gsak_wptExtension["gsak:UserSort"];
    this.gsak_watch = gsak_wptExtension["gsak:Watch"];

    this.gsak_latbeforecorrect = gsak_wptExtension["gsak:LatBeforeCorrect"];
    this.gsak_longbeforecorrect = gsak_wptExtension["gsak:LonBeforeCorrect"];
    this.gsak_statebeforecorrect = gsak_wptExtension["gsak:StateBeforeCorrect"];
    this.gsak_countybeforecorrect = gsak_wptExtension["gsak:CountyBeforeCorrect"];

    this.gsak_object_logimages = gsak_wptExtension["gsak:LogImages"];

    // synthesized css flags
    this.inWatchedCounty = ["Callaway", "Macon"].indexOf(this.gsak_county) >= 0;
    this.isGC = this.gsak_code.startsWith("GC");
    this.isCorrected = this.gsak_latbeforecorrect !== undefined;
    this.isUnavailable = this.cache_available !== "True" && this.isGC;
    this.isArchived = this.cache_archived === "True";

};

$(document).ready(function() {

    var Data = function(data) {
        var self = this;

        self.ContextMenuClick = function(event) { console.log(event); };

        self.GeocacheList = [];

        $.each(data.gpx.wpt, function(index, wpt) {
            var geocache = new Geocache(wpt)
            if (index === 2) {
                console.log(wpt);
                console.log(geocache);
            }
            self.GeocacheList.push(geocache)
        });

        // self.wptList = self.waypoint_list;

        // self.wptList = data.gpx.wpt;
        // self.lat = function(wpt) {
        //     return wpt["@lat"];
        // };
        // self.lon = function(wpt) {
        //     return wpt["@lon"];
        // };
        self.thList = [
            // "gsak_county",
            "gsak_usersort",
            "gsak_code",
            "type",
            // "cache_type",
            "link",
            // "cache_name",
            "lat",
            "lon",
            // "cache_archived",
            // "cache_available",
            // "cache_difficulty",
            // "cache_terrain",
            "cache_encoded_hints"
        ];

        self.synthesized_name = function(wpt) {

            var result = [
                // wpt.gsak_usersort,
                // wpt.type.replace("Geocache|", "").replace("Cache", ""),
                wpt.sym,
                wpt.name,
                wpt.desc
            ].join("/");

            return result;
        };

    };

    myData = new Data(data);

    ko.applyBindings(myData);
})
