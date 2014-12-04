// javascript template
// vim:ts=4:sw=4:tw=0:wm=0:et:nowrap

// Created:       Thu 04 Dec 2014 10:37:33 AM CST
// Last Modified: Thu 04 Dec 2014 02:56:17 PM CST

'use strict'

var fs = require('fs'),
    xml2js = require('xml2js');

var parser = new xml2js.Parser();

var results;

function getResults() {
    fs.readFile(__dirname + '/test.gpx', function(err, data) {
        if (err) { raise (err) };
        parser.parseString(data, function (err, results) {
            if (err) { raise (err) };

//          console.log("getResults is done");

//          console.dir(results);
//          console.log('Done');

//          var json_out = JSON.stringify(results, undefined, " ");
//          console.log(json_out);

            var wpts = results.gpx.wpt;
//          console.log(wpts[0]);
//          console.log(wpts.length);

            for(var i=0; i<wpts.length; i++) {

                var wpt = wpts[i];

                var lat = wpt.$['lat'];
                var lon = wpt.$['lon'];
                var time = wpt.time[0];
                var name = wpt.name[0];
                var desc = wpt.desc[0];
                var link = wpt.link[0];
                var link_href = link['$'].href;
                var link_text = link['text'][0];
                var sym = wpt.sym[0];
                var type = wpt.type[0];
                var extensions = wpt.extensions[0];
                var gsak_wptExtension = extensions['gsak:wptExtension'][0];
                var gsak_UserFlag = gsak_wptExtension["gsak:UserFlag"][0];
                var gsak_Lock = gsak_wptExtension["gsak:Lock"][0];
                var gsak_DNF = gsak_wptExtension["gsak:DNF"][0];
                var gsak_Watch = gsak_wptExtension["gsak:Watch"][0];
                var gsak_UserData = gsak_wptExtension["gsak:UserData"][0];
                var gsak_FirstToFind = gsak_wptExtension["gsak:FirstToFind"][0];
                var gsak_User2 = gsak_wptExtension["gsak:User2"][0];
                var gsak_User3 = gsak_wptExtension["gsak:User3"][0];
                var gsak_User4 = gsak_wptExtension["gsak:User4"][0];
                var gsak_County = gsak_wptExtension["gsak:County"][0];
                var gsak_UserSort = gsak_wptExtension["gsak:UserSort"][0];
                var gsak_SmartName = gsak_wptExtension["gsak:SmartName"][0];
                var gsak_LastGpxDate = (gsak_wptExtension["gsak:LastGpxDate"] || [ "1/1/1970" ])[0];
                var gsak_Code = gsak_wptExtension["gsak:Code"][0];
                var gsak_Resolution = gsak_wptExtension["gsak:Resolution"][0];
                var gsak_IsPremium = gsak_wptExtension["gsak:IsPremium"][0];
                var gsak_FavPoints = gsak_wptExtension["gsak:FavPoints"][0];
                var gsak_GcNote = gsak_wptExtension["gsak:GcNote"][0];
                var gsak_Guid = gsak_wptExtension["gsak:Guid"][0];
                var gsak_CacheImages = gsak_wptExtension["gsak:CacheImages"][0];
                var gsak_LogImages = gsak_wptExtension["gsak:LogImages"][0];
                var gsak_CustomData = gsak_wptExtension["gsak:CustomData"][0];
                var groundspeak_cache = extensions['groundspeak:cache'][0];
                var groundspeak_name = groundspeak_cache["groundspeak:name"][0];
                var groundspeak_placed_by = groundspeak_cache["groundspeak:placed_by"][0];
                var groundspeak_owner = groundspeak_cache["groundspeak:owner"][0];
                var groundspeak_type = groundspeak_cache["groundspeak:type"][0];
                var groundspeak_container = groundspeak_cache["groundspeak:container"][0];
                var groundspeak_attributes = groundspeak_cache["groundspeak:attributes"][0];
                var groundspeak_difficulty = groundspeak_cache["groundspeak:difficulty"][0];
                var groundspeak_terrain = groundspeak_cache["groundspeak:terrain"][0];
                var groundspeak_country = groundspeak_cache["groundspeak:country"][0];
                var groundspeak_state = groundspeak_cache["groundspeak:state"][0];
                var groundspeak_short_description = groundspeak_cache["groundspeak:short_description"][0];
                var groundspeak_long_description = groundspeak_cache["groundspeak:long_description"][0];
                var groundspeak_encoded_hints = groundspeak_cache["groundspeak:encoded_hints"][0];
                var groundspeak_logs = groundspeak_cache["groundspeak:logs"][0];
                var groundspeak_travelbugs = groundspeak_cache["groundspeak:travelbugs"][0];

                console.log("lat:", lat);
                console.log("lon:", lon);
                console.log("time:", time);
                console.log("desc:", desc);
                console.log("link:", link);
                console.log("  link_href:", link_href);
                console.log("  link_text:", link_text);
                console.log("sym:", sym);
                console.log("type:", type);
                console.log("extensions:"); // , JSON.stringify(extensions, undefined, " "));
                console.log("  gsak_wptExtension:"); // , JSON.stringify(gsak_wptExtension, undefined, " ")); 
                console.log("    gsak_UserFlag:", gsak_UserFlag );
                console.log("    gsak_Lock:", gsak_Lock );
                console.log("    gsak_DNF:", gsak_DNF );
                console.log("    gsak_Watch:", gsak_Watch );
                console.log("    gsak_UserData:", gsak_UserData );
                console.log("    gsak_FirstToFind:", gsak_FirstToFind );
                console.log("    gsak_User2:", gsak_User2 );
                console.log("    gsak_User3:", gsak_User3 );
                console.log("    gsak_User4:", gsak_User4 );
                console.log("    gsak_County:", gsak_County );
                console.log("    gsak_UserSort:", gsak_UserSort );
                console.log("    gsak_SmartName:", gsak_SmartName );
                console.log("    gsak_LastGpxDate:", gsak_LastGpxDate );
                console.log("    gsak_Code:", gsak_Code );
                console.log("    gsak_Resolution:", gsak_Resolution );
                console.log("    gsak_IsPremium:", gsak_IsPremium );
                console.log("    gsak_FavPoints:", gsak_FavPoints );
                console.log("    gsak_GcNote:", gsak_GcNote );
                console.log("    gsak_Guid:", gsak_Guid );
                console.log("    gsak_CacheImages:", JSON.stringify(gsak_CacheImages, undefined, " "));
                console.log("    gsak_LogImages:", JSON.stringify(gsak_LogImages, undefined, " "));
                console.log("    gsak_CustomData:", JSON.stringify(gsak_CustomData, undefined, " "));
                console.log("  groundspeak_cache:"); // , JSON.stringify(groundspeak_cache, undefined, " ")); 
                console.log("    groundspeak_name:", groundspeak_name);
                console.log("    groundspeak_placed_by:", groundspeak_placed_by);
                console.log("    groundspeak_owner:", groundspeak_owner);
                console.log("    groundspeak_type:", groundspeak_type);
                console.log("    groundspeak_container:", groundspeak_container);
                console.log("    groundspeak_attributes:", groundspeak_attributes);
                console.log("    groundspeak_difficulty:", groundspeak_difficulty);
                console.log("    groundspeak_terrain:", groundspeak_terrain);
                console.log("    groundspeak_country:", groundspeak_country);
                console.log("    groundspeak_state:", groundspeak_state);
                console.log("    groundspeak_short_description:", groundspeak_short_description);
                console.log("    groundspeak_long_description:", groundspeak_long_description);
                console.log("    groundspeak_encoded_hints:", groundspeak_encoded_hints);
                console.log("    groundspeak_logs:", JSON.stringify(groundspeak_logs, undefined, " "));
                console.log("    groundspeak_travelbugs:", JSON.stringify(groundspeak_travelbugs, undefined, " "));
            }

        });
    });
    return results;
};

getResults();

// exports.getResults = getResults;
