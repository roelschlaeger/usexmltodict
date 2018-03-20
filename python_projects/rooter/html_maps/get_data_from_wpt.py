#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:noic

"""Generate a list of (@lat, @lon, text, sym, UserSort, @href) tuples"""

########################################################################


def get_data_from_wpt(wpt):
    """Generate a list of (@lat, @lon, text, sym, UserSort, @href)
tuples"""

    result = []

    for wpt0 in wpt:
        link = wpt0["link"]
        extensions = wpt0["extensions"]
        gsak = extensions["gsak:wptExtension"]
        result.append(
            (
                wpt0["@lat"],
                wpt0["@lon"],
                link["text"],
                wpt0["sym"],
                wpt0["name"],
                gsak["gsak:UserSort"],
                link["@href"]
            )
        )

    return result


########################################################################

if __name__ == "__main__":

    from json import loads
    from pprint import pprint

    JSON_FILE = "outfile.json"

    with open(JSON_FILE, "rb") as JSONFILE:
        print(f"\nReading from {JSON_FILE}")
        DOC = loads(JSONFILE.read())

    GPX = DOC['gpx']
    WPT = GPX['wpt']

    RESULT = get_data_from_wpt(WPT)

    pprint(RESULT)

# end of file
