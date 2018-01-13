"""Parse a .gpx file into a .csv output."""

from __future__ import print_function

from bs4 import BeautifulSoup
from collections import OrderedDict
from json import loads
import csv

from with_sqlite3 import create_temp_db, delete_temp_db, fill_temp_db

# database file
DB_FILE = "output_file.db"

# input filename
JSONFILE = "outfile.json"

# output filename
CSV_FILENAME = "temp.csv"

# interesting columns
W0_COLS = [
    "@lat",
    "@lon",
    "name",
    "desc",
    "sym",
    "type"
]

LINK_COLS = [
    "@href",
    "text"
]

# these are keys underneath [extensions]
WPTEXTENSION_COLS = [
    "gsak:User2",
    "gsak:UserSort",
    "gsak:Code"
]

CACHE_COLS = [
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

########################################################################


def fix_html(d, key_list):
    """Extract text from hint and description tags"""
    for key in key_list:
        text = ""
        if key == "groundspeak:encoded_hints" and d[key] != "None":
            text = d[key]
        else:
            if d[key] is not None:
                if "#text" in d[key]:
                    text = d[key]["#text"]
                    if "@html" in d[key] and d[key]["@html"]:
                        soup = BeautifulSoup(text, 'html.parser')
                        text = soup.get_text()
        d[key] = text

########################################################################


def build_row(w0):
    """Create a new output row from the column specs"""
    d = OrderedDict()
    for c in W0_COLS:
        d[c] = w0[c]
    for c in LINK_COLS:
        d[c] = w0["link"][c]
    for c in WPTEXTENSION_COLS:
        d[c] = w0["extensions"]["gsak:wptExtension"][c]
    for c in CACHE_COLS:
        d[c] = w0["extensions"]["groundspeak:cache"][c]

    # make corrections to text fields
    fix_html(
        d,
        [
            "groundspeak:short_description",
            "groundspeak:long_description",
            "groundspeak:encoded_hints",
        ]
    )

    # return the row
    return d

########################################################################


def create_temp_csv(filename, wpt):
    """Create a temp.csv file containing select gpx columns"""

    with open(filename, "w") as f:

        # create the spreadsheet writer
        writer = csv.writer(
            f, lineterminator='\n', dialect="excel-tab"
        )

        # fill in spreadsheet header and rows
        for index, w0 in enumerate(wpt):
            row = build_row(w0)
            if index == 0:
                writer.writerow(row.keys())
            writer.writerow(row.values())

########################################################################

def main(input_file, output_file, create=False, delete=False):

    with open(input_file, "rb") as jsonfile:
        print(f"\nReading from {input_file}")
        doc = loads(jsonfile.read())

    gpx = doc['gpx']
    wpt = gpx['wpt']

    if delete:
        print("\nDeleting table in %s" % DB_FILE)
        delete_temp_db(DB_FILE)

    if create:
        print("\nCreating and filling table in %s" % DB_FILE)
        row = build_row(wpt[0])
        create_temp_db(DB_FILE, row)
        for w0 in wpt:
            row = build_row(w0)
            fill_temp_db(DB_FILE, row)
    else:
        if not delete:
            print(f"\nWriting to {output_file}.")
            create_temp_csv(output_file, wpt)


########################################################################

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Convert JSON file to CSV",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "inputfile",
        type=str,
        nargs="?",
        help="JSON input filename",
    )

    parser.add_argument(
        "csvfile",
        type=str,
        nargs="?",
        help="CSV output filename",
    )

    parser.set_defaults(
        inputfile=JSONFILE,
        csvfile=CSV_FILENAME
    )

    parser.add_argument(
        "-c",
        "--create",
        action="store_true",
        help="create new database table and exit",
    )

    parser.add_argument(
        "-d",
        "--delete",
        action="store_true",
        help="delete database table",
    )

    args = parser.parse_args()

    main(
        args.inputfile,
        args.csvfile,
        args.create,
        args.delete
    )

# end of file
