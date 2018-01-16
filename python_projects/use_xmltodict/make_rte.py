from collections import OrderedDict

# ordered list of keys that are available in WPT entries
KEYS = [
    '@lat',
    '@lon',
    # 'time',
    'name',
    'desc',
    # 'link',
    # 'sym',
    # 'type',
    # 'extensions'
]


def make_rte(wpt):
    rte = OrderedDict()
    rte["name"] = "name"
    rte["cmt"] = "cmt"
    rte["desc"] = "desc"
    rte["src"] = "src"
    rte["link"] = "link"
    rte["number"] = "number"
    rte["type"] = "type"
    rte["extensions"] = "extensions"

    rtept = []
    for w0 in wpt:
        r0 = OrderedDict.fromkeys(KEYS)
        for key in KEYS:
            r0[key] = w0[key]
        rtept.append(r0)

    rte["rtept"] = rtept

    return rte


if __name__ == "__main__":

    import argparse
    from xmltodict import parse, unparse

    FILENAME = "topo925 - Charleston IL.gpx"
    OUTFILENAME = FILENAME.replace(".gpx", " route.gpx")

    def main(filename):

        # print(f"\nReading from {filename}.\n")
        jsontext = open(filename, "rb").read()
        doc = parse(jsontext)
        gpx = doc["gpx"]
        wpt = gpx["wpt"]

        rte = make_rte(wpt)
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
