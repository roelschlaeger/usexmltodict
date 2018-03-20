#!/usr/bin/env python

"""Parse a .gpx file into a .csv output."""

from __future__ import print_function

from json import loads
import csv
from collections import OrderedDict
from bs4 import BeautifulSoup

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


def fix_html(e_dict, key_list):
    """Extract text from hint and description tags"""
    for key in key_list:
        text = ""

        if key == "groundspeak:encoded_hints" and e_dict[key] != "None":
            text = e_dict[key]

        else:
            if e_dict[key] is not None:
                if "#text" in e_dict[key]:
                    text = e_dict[key]["#text"]
                    if "@html" in e_dict[key] and e_dict[key]["@html"]:
                        soup = BeautifulSoup(text, 'html.parser')
                        text = soup.get_text()

        e_dict[key] = text

########################################################################


def build_row(wpt0):
    """Create a new output row from the column specs"""
    e_dict = OrderedDict()
    for column in W0_COLS:
        e_dict[column] = wpt0[column]
    for column in LINK_COLS:
        e_dict[column] = wpt0["link"][column]
    for column in WPTEXTENSION_COLS:
        e_dict[column] = wpt0["extensions"]["gsak:wptExtension"][column]
    for column in CACHE_COLS:
        e_dict[column] = wpt0["extensions"]["groundspeak:cache"][column]

    # make corrections to text fields
    fix_html(
        e_dict,
        [
            "groundspeak:short_description",
            "groundspeak:long_description",
            "groundspeak:encoded_hints",
        ]
    )

    # return the row
    return e_dict

########################################################################


def create_temp_csv(filename, wpt):
    """Create a temp.csv file containing select gpx columns"""

    with open(filename, "w") as outfile:

        # create the spreadsheet writer
        writer = csv.writer(
            outfile, lineterminator='\n', dialect="excel-tab"
        )

        # fill in spreadsheet header and rows
        for index, wpt0 in enumerate(wpt):
            row = build_row(wpt0)
            if index == 0:
                writer.writerow(row.keys())
            writer.writerow(row.values())

########################################################################


def main(input_file, output_file, create=False, delete=False):
    """Processing to read JSON-formatted 'input_file" to generate 'output_file'
    HTML maps file

    Arguments:
        input_file {str} -- input filename
        output_file {str} -- output filename

    Keyword Arguments:
        Delete and/or create a 'waypoints' table in the SQLite3 file
        'output_file.db':

        delete {bool} -- if True delete database table (default: {False})
        create {bool} -- if True create a database table (default: {False})
    """

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
        for wpt0 in wpt:
            row = build_row(wpt0)
            fill_temp_db(DB_FILE, row)
    else:
        if not delete:
            print(f"\nWriting to {output_file}.")
            create_temp_csv(output_file, wpt)


########################################################################

if __name__ == "__main__":

    import argparse

    PARSER = argparse.ArgumentParser(
        description="Convert JSON file to CSV",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    PARSER.add_argument(
        "inputfile",
        type=str,
        nargs="?",
        help="JSON input filename",
    )

    PARSER.add_argument(
        "csvfile",
        type=str,
        nargs="?",
        help="CSV output filename",
    )

    PARSER.set_defaults(
        inputfile=JSONFILE,
        csvfile=CSV_FILENAME
    )

    PARSER.add_argument(
        "-c",
        "--create",
        action="store_true",
        help="create new database table and exit",
    )

    PARSER.add_argument(
        "-d",
        "--delete",
        action="store_true",
        help="delete database table",
    )

    ARGS = PARSER.parse_args()

    main(
        ARGS.inputfile,
        ARGS.csvfile,
        ARGS.create,
        ARGS.delete
    )

# end of file
