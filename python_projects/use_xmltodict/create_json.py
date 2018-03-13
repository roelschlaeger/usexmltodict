# create a JSON file from a .gpx file
"""
create_json.py

Convert .gpx file to JSON

usage: create_json.py [-h ]
       create_json.py [-i INPUTFILE ] [-j JSONFILE ]
       create_json.py [ INPUTFILE [ JSONFILE ] ]
       create_json.py --version

optional arguments:
  -h, --help                 show this help message and exit
  -i, --inputfile INPUTFILE  GPX input filename [default: topo930a - Smithshire IL.gpx]
  -j, --jsonfile JSONFILE    JSON output filename [default: outfile.json]
  --version                  Display program version and exit

"""


import json
from xmltodict import parse

########################################################################


def create_outfile_json(doc, outfile):
    """Create a JSON file in outfile describing doc"""

    # create the JSON string
    s = json.dumps(doc, indent=1)

    # write it to a text file
    with open(outfile, "w") as ofile:
        ofile.write(s)

    # show that processing is complete
    print(f"JSON written to {outfile}")

########################################################################


def get_creation_info(doc):
    """Get file creation from metadata
    
    Arguments:
        doc {dict} -- dict-converted GPX information
    
    Returns:
        str -- comma-delimited string of 'desc' and 'time' metadata
    """
    gpx = doc["gpx"]
    return ", ".join([gpx["metadata"][x] for x in ["desc", "time"]])


########################################################################


def create_json(filename, outfile):
    """Create a JSON file named 'outfile' from .gpx input 'filename'
    
    Arguments:
        filename {str} -- input filename for .gpx file
        outfile {str} -- output filename for .json file
    """

    print(f"\nReading from {filename}, writing to {outfile}.\n")
    jsontext = open(filename, "rb").read()
    doc = parse(jsontext)
    print(get_creation_info(doc))
    create_outfile_json(doc, outfile)


########################################################################

if __name__ == "__main__":

    # import argparse

    # # FILENAME = "temp.gpx"
    # FILENAME = "topo930a - Smithshire IL.gpx"
    # OUTFILE = "outfile.json"

    # parser = argparse.ArgumentParser(
    #     description="Convert .gpx file to JSON",
    #     formatter_class=argparse.ArgumentDefaultsHelpFormatter
    # )

    # parser.add_argument(
    #     "inputfile",
    #     type=str,
    #     nargs="?",
    #     help="GPX input filename",
    # )

    # parser.add_argument(
    #     "jsonfile",
    #     type=str,
    #     nargs="?",
    #     help="JSON output filename",
    # )

    # parser.set_defaults(
    #     inputfile=FILENAME,
    #     jsonfile=OUTFILE
    # )

    # args = parser.parse_args()

    # create_json(args.inputfile, args.jsonfile)

    from docopt import docopt

    arguments = docopt(__doc__, version="0.1.0")
    print(arguments)

    # from create_json import create_json
    inputfile = arguments["INPUTFILE"] or arguments["--inputfile"]
    jsonfile = arguments["JSONFILE"] or arguments["--jsonfile"]
    # print(f"create_json({inputfile}, {jsonfile})")
    create_json(inputfile, jsonfile)

# end of file
