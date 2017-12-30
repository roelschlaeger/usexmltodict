# create a JSON file from a .gpx file

import json
from xmltodict import parse

########################################################################


def create_outfile_json(doc, outfile):
    """Create a JSON file in outfile describing doc"""

    # create the JSON string
    s = json.dumps(doc, indent=1)

    # write it to a text file
    with open(OUTFILE, "w") as ofile:
        ofile.write(s)

    # show that processing is complete
    print(f"JSON written to {outfile}")

########################################################################


def main(filename, outfile):

    print(f"\nReading from {filename}, writing to {outfile}.\n")
    jsontext = open(filename, "rb").read()
    doc = parse(jsontext)
    create_outfile_json(doc, outfile)


########################################################################

if __name__ == "__main__":

    import argparse

    FILENAME = "temp.gpx"
    OUTFILE = "outfile.json"

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

    parser.add_argument(
        "jsonfile",
        type=str,
        nargs="?",
        help="JSON output filename",
    )

    parser.set_defaults(
        inputfile=FILENAME,
        jsonfile=OUTFILE
    )

    args = parser.parse_args()

    main(args.inputfile, args.jsonfile)

# end of file
