# vim:ts=4:sw=4:tw=0:wm=0:et

"""Ask for directions in Google Maps

    https://www.google.com/maps/dir/?api=1
"""

from build_path import build_paths


def directions(lats, lons, names, start, end, waypoints):
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


if __name__ == "__main__":

    from with_sqlite3 import get_data
    import myhtml

    FILENAME = "output_file.db"
    data = get_data(FILENAME)
    lats, lons, texts, syms, names, usersorts = zip(*data)

    doc = myhtml.XHTML("html")
    doc.meta(charset="utf-8")
    doc.title("Title for Route")
    doc.style("""
table, caption, th, td {
              border: 1px solid black;
              border-collapse: collapse;
              vertical-align: center;
              padding: 3px;
              }
caption { font-weight: bold; font-size: 150% }
th { text-align: center; font-size: 125%}
""")

    table = doc.body.table()
    table.caption("Table of Map Routes")

    tr = table.thead.tr()
    tr.th("UserSort")
    tr.th("From")
    tr.th("To")
    tr.th("Via")

    for start, end, waypoints in build_paths(data):
        tr = table.tr()
        href = directions(lats, lons, names, start, end, waypoints)
        tr.td(str(usersorts[start]), style="text-align: center")
        tr.td.a(texts[start], href=href, target="_blank")
        tr.td(texts[end])
        td3 = tr.td()
        if waypoints:
            if len(waypoints) == 1:
                td3(texts[waypoints[0]])
            else:
                for index, waypoint in enumerate(waypoints):
                    if index == 0:
                        td3(texts[waypoint])
                    else:
                        td3.br()
                        td3(texts[waypoint])

    print("<!DOCTYPE HTML>\n" + str(doc))

# end of file
