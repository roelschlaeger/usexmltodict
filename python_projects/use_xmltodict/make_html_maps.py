#!/usr/bin/env python
"""
make_html_maps.py

Create a HTML file containing a table of Google directions for each leg of a journey described by the input .gpx file.

Usage: make_html_maps.py [ options ][ FILENAME... ]

Options:
    -h, --help  Display this help
    --version   Show program version
    FILENAME    .gpx filename(s) to be processed [default: ./topo930a - Smithshire.gpx ]
"""

from create_json import create_json
from directions import convert_json_to_html


########################################################################


def make_html_map(filename):
    print(filename)
    json_filename = filename + ".json"
    html_filename = json_filename + ".html"
    create_json(filename, json_filename)
    convert_json_to_html(json_filename, html_filename)


########################################################################


if __name__ == "__main__":

    from docopt import docopt

    arguments = docopt(__doc__, version="0.0.1")

    if not arguments["FILENAME"]:
        arguments["FILENAME"] = ["topo930a - Smithshire IL.gpx"]

    print(arguments)

    for filename in arguments["FILENAME"]:
        make_html_map(filename)

# end of file
