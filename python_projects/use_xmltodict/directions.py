# vim:ts=4:sw=4:tw=0:wm=0:et

"""Ask for directions in Google Maps

    https://www.google.com/maps/dir/?api=1
"""

# from urllib.parse import urlencode
# from collections import defaultdict

def directions(pfm, pto, waypoints=None):
    """Encode string for directions request"""
    s = "https://www.google.com/maps/dir/?api=1"
    s += "&origin=%s,%s" % (pfm[0], pfm[1])
    s += "&destination=%s,%s" % (pto[0], pto[1])
    if waypoints:
        w = "&waypoints="
        for index, wpt in enumerate(waypoints):
            if index == 0:
                w += "%s,%s" % (wpt[0], wpt[1])
            else:
                w += "%7C%s,%s" % (wpt[0], wpt[1])
        s += w
#   print(s)
    return s


if __name__ == "__main__":

    import myhtml

    doc = myhtml.HTML()
    table = doc.body.table(border="1")
    tr = table.tr()
    tr.th("Index")
    tr.th("From")
    tr.th("To")
    tr.th("Link")

    from with_sqlite3 import get_data
    FILENAME = "output_file.db"

    data = get_data(FILENAME)

    for index, item in enumerate(data):
        tr = table.tr()
        lat, lon, text, sym, name = item[:5]
        p_to = (lat, lon, name, text)
        if index == 0:
            p_from = p_to
            waypoints = []
            continue
        tr.th(str(index))
        tr.th(p_from[2])
        tr.th(p_to[2])
        href = directions(p_from[:2], p_to[:2])
        tr.th.a("link", href=href, type="text/html")
        p_from = p_to

    print(doc)

# end of file
