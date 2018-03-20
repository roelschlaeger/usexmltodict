#!/usr/bin/env python
"""
make_html_maps.py

Create a HTML file containing a table of Google directions for each leg
of a journey described by the input .gpx file.

Usage: make_html_maps.py [ options ][ FILENAME... ]

Options:
    -h, --help  Display this help
    --version   Show program version
    FILENAME    .gpx filename(s) to be processed [default: ./topo931a - Saint James MO.gpx]
"""

import os.path
from html_maps.create_json import create_json
from html_maps.directions import convert_json_to_html

########################################################################


def make_html_map(filename, debug=True):
    """ Create a HTML file containing a generated table of URL links to
    Google Maps to draw segments of the route contained in the
    'filename' .gpx file.

    Arguments: filename {str} -- the name of the .gpx file containing
        the ordered route
    """
    if debug:
        print(filename)

    json_filename = filename + ".json"
    # assert not os.path.exists(json_filename), f"Invalid intermediate filename: {json_filename}"
    # if os.path.exists(json_filename):
    #     raise FileExistsError(f"Invalid intermediate filename:\n   {json_filename}")

    html_filename = json_filename + ".html"
    # if os.path.exists(html_filename):
    #     raise FileExistsError(f"File exists: {html_filename}")

    create_json(filename, json_filename)
    convert_json_to_html(json_filename, html_filename)

    # remove the temporary file
    os.remove(json_filename)


########################################################################


def process_arg(filename):
    """Provide a common interface for use by sextus.py

    Arguments:
        filename {str} -- name of file to be processed
    """
    try:
        make_html_map(filename, debug=False)
    except FileExistsError as error:
        print(error)

########################################################################


if __name__ == "__main__":

    from docopt import docopt

    ARGUMENTS = docopt(__doc__, version="0.0.1")

    if not ARGUMENTS["FILENAME"]:
        ARGUMENTS["FILENAME"] = ["topo931a - Saint James MO.gpx"]

    print(ARGUMENTS)

    for FILENAME in ARGUMENTS["FILENAME"]:
        make_html_map(FILENAME)

# end of file
