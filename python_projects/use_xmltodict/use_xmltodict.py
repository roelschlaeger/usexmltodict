from contextlib import redirect_stdout
from xmltodict import parse
import csv
import json

FILENAME = "temp.gpx"
JSONFILE = "outfile.json"
TEXTFILE = "outfile.txt"
JSONTEXT = open(FILENAME, "rb").read()


def create_outfile_json(doc):
    """Create a JSON file describing doc"""
    s = json.dumps(doc, indent=1)
    with open("outfile.json", "w") as ofile:
        ofile.write(s)
    print("JSON written to %s" % JSONFILE)


def create_temp_csv(wpt):
    """Create a temp.csv file containing select gpx columns"""
    w0_cols = ["@lat", "@lon", "name", "desc", "sym", "type"]
    link_cols = ["@href", "text"]
#   extension_cols = ["gsak:wptExtension", "groundspeak:cache"]
    wptExtension_cols = ["gsak:User2", "gsak:UserSort", "gsak:Code"]
    cache_cols = [
        "@available",
        "@archived",
        "groundspeak:placed_by",
        "groundspeak:type",
        "groundspeak:container",
        "groundspeak:difficulty",
        "groundspeak:terrain",
        "groundspeak:short_description",
        "groundspeak:long_description",
        "groundspeak:encoded_hints",
    ]

    col_lists = [
        w0_cols,
        link_cols,
        wptExtension_cols,
        cache_cols
    ]

    cols = []
    [cols.extend(l) for l in col_lists]
#   pprint(cols)

    def build_row(w0):
        cols = []
        cols.extend(w0[c] for c in w0_cols)
        cols.extend(w0["link"][c] for c in link_cols)
        cols.extend(
            w0["extensions"]["gsak:wptExtension"][c]
            for c in wptExtension_cols
        )
        cols.extend(
            w0["extensions"]["groundspeak:cache"][c] for c in cache_cols
        )
        return cols

    with open("temp.csv", "w") as f:
        with redirect_stdout(f):
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(cols)
            for w0 in wpt:
                row = build_row(w0)
                writer.writerow(row)


def show(s):
    """Show the contents of an OrderedDict"""
    for k in s.keys():
        print(bytes(k, 'utf8'), str(s[k])[:80])


# redirect stdout to a file
with open(TEXTFILE, "w") as outfile:

    doc = parse(JSONTEXT)
    # create_outfile_json(doc)

    gpx = doc['gpx']
    wpt = gpx['wpt']
    w0 = wpt[0]

#   print("Output is going to %s" % TEXTFILE)
#   with redirect_stdout(outfile):

#       show(gpx)
#       show(w0)
#       for w in wpt:
#           show(w)

#       print("Done 1!")

    create_temp_csv(wpt)

    print("Done 2!")

print("Done 3!")

# end of file
