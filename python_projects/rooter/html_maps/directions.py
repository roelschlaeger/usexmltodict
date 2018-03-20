# vim:ts=4:sw=4:tw=0:wm=0:et:noic

"""Ask for directions in Google Maps

    https://www.google.com/maps/dir/?api=1
"""

########################################################################

import datetime
import sys
from json import loads
import pml
from html_maps.build_path import build_paths
from html_maps.get_data_from_wpt import get_data_from_wpt

JSON_INPUT_FILENAME = "outfile.json"
HTML_OUTPUT_FILENAME = "directions.html"

########################################################################

BOOTSTRAP_LINK = """<link
rel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"
>"""

JQUERY = """<script
src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js">
</script>"""

BOOTSTRAP = """<script
src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js">
</script>"""

STYLE = """
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
    vertical-align: center;
    padding: 3px;
    }
th {
    text-align: center;
    font-size: 125%
    }
h2 {
    text-align: center;
    }
hr {
    border-width: 4px;
}
"""

SCRIPT = """
$(document).ready(function(){
    $(".btn").click(function(){
        $(this).addClass("btn-warning").removeClass("btn-primary");
    });
    $("#bobs_reset").click(function(){
        $(".btn-warning").addClass("btn-primary").removeClass("btn-warning");
    });
});
"""

########################################################################


def directions(
        lats=None,
        lons=None,
        start=None,
        end=None,
        waypoints=None
):
    """Create URI for a map from 'start' to 'end' via possibly empty
'waypoints' list of intermediate points"""

    result = "https://www.google.com/maps/dir/?api=1"
    result += "&origin=%s,%s" % (lats[start], lons[start])
    result += "&destination=%s,%s" % (lats[end], lons[end])
    if waypoints:
        waypoints_string = "&waypoints="
        for index, wpt in enumerate(waypoints):
            if index != 0:
                waypoints_string += "%7C"
            waypoints_string += "%s,%s" % (lats[wpt], lons[wpt])
        result += waypoints_string
    return result

########################################################################


def build_map_table_html(data):
    """Create a HTML file containing a table of links to maps for each segment
of the route going from geocache to geocache.

    data is a list of (lat, lon, text, sym, name, usersort, href) tuples.
"""

    lats, lons, texts, syms, names, usersorts, hrefs = zip(*data)
    del syms  # not needed
    del names  # not needed

    doc = pml.XHTML("html")

    today = datetime.date.today()
    doc.title(f"Generated by {__file__} on {today}.")

    doc.meta(charset="utf-8")
    doc.meta(name="viewport", content="width=device-width, initial-scale=1")

    doc += BOOTSTRAP_LINK
    doc += JQUERY
    doc += BOOTSTRAP

    doc.style(STYLE)

    doc.script(SCRIPT)

    body = doc.body()
    body.h2(f"Created {today} by {__file__}.")
    body.hr()

    div = body.div(klass="container")
    div.h2("Table of Map Routes")
    table = div.table(klass="table")

    thead = table.thead()
    tr0 = thead.tr()
    tr0.th("Link", colspan="1")
    tr0.th("Waypoints", colspan="2")

    tr1 = thead.tr()
    tr1.th("To: UserSort")
    tr1.th("Name")
    tr1.th("Via Names")

    tbody = table.tbody()

    for item_index, items in enumerate(build_paths(data)):
        start, end, waypoints = items

        # show phony header row just for route starting point
        if item_index == 0:
            tr2 = tbody.tr()
            tr2.td.button(
                "Reset: %s" % usersorts[start],
                klass="btn btn-primary",
                id="bobs_reset"
            )
            tr2.td(texts[start])
            tr2.td()

        tr3 = tbody.tr()

        href = directions(
            lats=lats,
            lons=lons,
            start=start,
            end=end,
            waypoints=waypoints
        )

        tr3.td.a(
            "%s" % (usersorts[end]),
            href=href,
            target="_blank",
            type="button",
            klass="btn btn-primary"
        )

        if hrefs[end]:
            tr3.td.a(
                texts[end],
                href=hrefs[end],
                target="_blank"
            )
        else:
            tr3.td(texts[end])

        td3 = tr3.td()
        if waypoints:
            for index, waypoint in enumerate(waypoints):
                if index != 0:
                    td3.br()
                td3 += texts[waypoint]

    return "<!DOCTYPE HTML>\n" + str(doc)

########################################################################


def convert_json_to_html(
        json_filename=JSON_INPUT_FILENAME,
        html_filename=HTML_OUTPUT_FILENAME
):
    """Convert .gpx data encoded in json_filename to HTML directions in
html_filename."""

    print(
        f"Reading from {json_filename}, writing to {html_filename}",
        file=sys.stderr
    )

    with open(json_filename, "rb") as jsonfile:
        doc = loads(jsonfile.read())

    with open(html_filename, "w") as html_output_file:
        print(
            build_map_table_html(get_data_from_wpt(doc["gpx"]["wpt"])),
            file=html_output_file
        )

########################################################################


if __name__ == "__main__":

    import argparse

    PARSER = argparse.ArgumentParser(
        description="Convert .JSON file of GPX data to HTML",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    PARSER.add_argument(
        "inputfile",
        type=str,
        nargs="?",
        help="JSON input filename",
    )

    PARSER.add_argument(
        "htmlfile",
        type=str,
        nargs="?",
        help="HTML output filename",
    )

    PARSER.set_defaults(
        inputfile=JSON_INPUT_FILENAME,
        htmlfile=HTML_OUTPUT_FILENAME
    )

    ARGS = PARSER.parse_args()

    JSON_FILENAME = ARGS.inputfile
    HTML_FILENAME = ARGS.htmlfile

    convert_json_to_html(JSON_FILENAME, HTML_FILENAME)

# end of file
