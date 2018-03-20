#!/usr/bin/env python
# create a JSON file from a .gpx file
"""
create_json.py

Convert a .gpx file to JSON

usage: create_json.py [-d -h ]
       create_json.py [-i INPUTFILE ] [-j JSONFILE ]
       create_json.py [ INPUTFILE [ JSONFILE ] ]
       create_json.py --version

optional ARGUMENTS:
  -d, --debug                show debugging information
  -h, --help                 show this help message and exit.
  -i, --inputfile INPUTFILE  GPX input filename
                             [default: topo931a - Saint James MO.gpx].
  -j, --jsonfile JSONFILE    JSON output filename
                             [default: outfile.json].
  --version                  display program version and exit.

"""

__VERSION__ = "0.1.0"


import json
from xmltodict import parse

########################################################################


def create_outfile_json(doc, outfile, debug=False):
    """Create a JSON file describing 'doc' in 'outfile'

    Arguments:
        doc {str} -- file name of document to be converted
        outfile {str} -- filename of output file
    """
    # create the JSON string
    dump_string = json.dumps(doc, indent=1)

    # write it to a text file
    with open(outfile, "w") as ofile:
        ofile.write(dump_string)

    if debug:
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


def create_json(filename, outfile, debug=False):
    """Create a JSON file named 'outfile' from .gpx input 'filename'

    Arguments:
        filename {str} -- input filename for .gpx file
        outfile {str} -- output filename for .json file
    """

    if debug:
        print(f"\nReading from {filename}, writing to {outfile}.")
    jsontext = open(filename, "rb").read()
    doc = parse(jsontext)
    if debug:
        print(get_creation_info(doc))
    create_outfile_json(doc, outfile, debug)


########################################################################

if __name__ == "__main__":

    from docopt import docopt

    ARGUMENTS = docopt(__doc__, version=__VERSION__)
    print(ARGUMENTS)

    # from create_json import create_json
    INPUTFILE = ARGUMENTS["INPUTFILE"] or ARGUMENTS["--inputfile"]
    JSONFILE = ARGUMENTS["JSONFILE"] or ARGUMENTS["--jsonfile"]
    # debug = ARGUMENTS["--debug"]
    # print(f"create_json({INPUTFILE}, {JSONFILE})")
    create_json(INPUTFILE, JSONFILE, debug=ARGUMENTS["--debug"])

# end of file
