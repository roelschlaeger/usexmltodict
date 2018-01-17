# vim:ts=4:sw=4:tw=0:wm=0:et:noic

from collections import OrderedDict

# count of the number of routes generated so far
global ROUTE_NUMBER
ROUTE_NUMBER = 0

# ordered list of keys that are available in WPT entries
KEYS = [
    '@lat',
    '@lon',
    # 'time',
    'name',
    'desc',
    'link',
    # 'sym',
    # 'type',
    # 'extensions'
]


def make_rte(wpt, **kwargs):

    if "route_number" in kwargs:
        route_number = kwargs["route_number"]
    else:
        global ROUTE_NUMBER

        # bump the route number
        ROUTE_NUMBER += 1
        # and use it
        route_number = ROUTE_NUMBER

    # the list of permitted keys and their default values
    optional_args = {
        "name": None,
        "cmt": None,
        "desc": None,
        "src": None,
        "link": None,
        "number": str(route_number),
        "type": "Route",
        "extensions": None
    }

    keys = optional_args.keys()
    optional_args.update(**kwargs)

    rte = OrderedDict()

    for key in keys:
        if optional_args[key]:
            rte[key] = optional_args[key]

    rtept = []
    for w0 in wpt:
        r0 = OrderedDict.fromkeys(KEYS)
        for key in KEYS:
            r0[key] = w0[key]

        usersort = w0["extensions"]["gsak:wptExtension"]["gsak:UserSort"]
        r0["name"] = "%s: %s" % (usersort, w0["name"])

        rtept.append(r0)

    rte["rtept"] = rtept

    return rte


if __name__ == "__main__":

    import argparse
    from xmltodict import parse, unparse

    FILENAME = "topo925a - Charleston IL.gpx"
    OUTFILENAME = FILENAME.replace(".gpx", " route.gpx")

    def main(filename):

        jsontext = open(filename, "rb").read()
        doc = parse(jsontext)
        gpx = doc["gpx"]
        wpt = gpx["wpt"]

        rte = make_rte(
            wpt,
            name="The name of the route",
            desc="The description of the route"
        )
        gpx["rte"] = rte
        doc["gpx"] = gpx

        with open(OUTFILENAME, "wb") as outputfile:
            unparse(doc, pretty=True, output=outputfile)

            print("Route written to %s" % OUTFILENAME)

    ########################################################################

    parser = argparse.ArgumentParser(
        description="Convert .gpx file to JSON",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "inputfile",
        type=str,
        nargs="?",
        help="GPX input filename",
    )

    parser.set_defaults(
        inputfile=FILENAME
    )

    args = parser.parse_args()

    main(args.inputfile)

# end of file
