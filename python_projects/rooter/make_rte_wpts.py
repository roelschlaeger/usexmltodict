# -*- coding utf-8 -*-
"""
Create a collection of <wpt> Elements.

Copyright (c) 2016-2017 Robert Oelschlaeger All Rights Reserved
roelsch2009@gmail.com
"""

#######################################################################

from __future__ import print_function

import sys
from pprint import pprint
from xml.etree import ElementTree as ET

assert sys.version_info > (3, ), "Python 3 required"

__VERSION__ = "0.0.2"
__DATE__ = "2017-07-28"

#######################################################################


def get_wpts(root):
    """Return a collection of <wpt> Elements from <root>."""
    wpt_tag = root.tag.replace("gpx", "wpt")
    wpts = root.findall(wpt_tag)
    return wpts

#######################################################################


def print_children(_w0):
    """Print the children nodes of the L{_w0} Element."""
    pprint(_w0.getchildren())
    for item in _w0.getchildren():
        print("'%s' : '%s'" % (item.tag.split("}")[1], item.text))

#######################################################################


def name_desc_dict(wpts):
    """Return a dictionary of (name, desc) pairs from L{wpts}."""
    wpt_tag = wpts[0].tag
    name_tag = wpt_tag.replace("wpt", "name")
    desc_tag = wpt_tag.replace("wpt", "desc")
    names = dict(
        (
            wpt.find(name_tag).text,
            wpt.find(desc_tag).text
        ) for wpt in wpts
    )

    return names

#######################################################################


if __name__ == "__main__":

    #######################################################################

    def main():
        """Main test routine."""

        infile = "default.gpx"

        tree = ET.parse(infile)
        root = tree.getroot()
        wpts = get_wpts(root)

        _w0 = wpts[0]
        print_children(_w0)

        names = name_desc_dict(wpts)
        pprint(names)

        return 0

    #######################################################################

    import time
    import argparse
    import textwrap

    try:
        START_TIME = time.time()

        PARSER = argparse.ArgumentParser(
            usage=textwrap.dedent(__doc__)
            )

        PARSER.add_argument(
            "--version",
            action="version",
            version="%%(prog)s, Version: %s %s" % (__VERSION__, __DATE__)
            )

        PARSER.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
            )

        OPTIONS = PARSER.parse_args()
        ARGS = None

        if OPTIONS.verbose:
            print(time.asctime())

        EXIT_CODE = main()

        if EXIT_CODE is None:
            EXIT_CODE = 0

        if OPTIONS.verbose:
            print(time.asctime())
            print('TOTAL TIME IN MINUTES:',)
            print((time.time() - START_TIME) / 60.0)

        sys.exit(EXIT_CODE)

    except KeyboardInterrupt as _error:      # Ctrl-C
        raise _error

    except SystemExit as _error:             # sys.exit()
        raise _error

    # except Exception as _error:
    #     print('ERROR, UNEXPECTED EXCEPTION')
    #     print(str(_error))
    #     traceback.print_exc()
    #     os._exit(1)

# end of file
