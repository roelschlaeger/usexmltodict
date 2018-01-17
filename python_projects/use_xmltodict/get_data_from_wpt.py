# vim:ts=4:sw=4:tw=0:wm=0:et:noic

########################################################################


def get_data_from_wpt(wpt):
    """Generate a list of (@lat, @lon, text, sym, UserSort, @href)
tuples"""

    result = []

    for w0 in wpt:
        link = w0["link"]
        extensions = w0["extensions"]
        gsak = extensions["gsak:wptExtension"]
        result.append(
            (
                w0["@lat"],
                w0["@lon"],
                link["text"],
                w0["sym"],
                w0["name"],
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

    with open(JSON_FILE, "rb") as jsonfile:
        print(f"\nReading from {JSON_FILE}")
        doc = loads(jsonfile.read())

    gpx = doc['gpx']
    wpt = gpx['wpt']

    result = get_data_from_wpt(wpt)

    pprint(result)

# end of file
