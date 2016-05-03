#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Tue 03 May 2016 09:33:16 AM CDT
# Last Modified: Tue 03 May 2016 11:34:17 AM CDT

"""
SYNOPSIS

    TODO helloworld [-h | --help] [-v | --version] [--verbose]

DESCRIPTION

    TODO This describes how to use this script.
    This docstring will be printed by the script if there is an error or
    if the user requests help (-h or --help).

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

VERSION

"""

from __future__ import print_function

__VERSION__ = "0.0.1"

########################################################################

from PIL import Image

HOLLERITH_ROWS = 12
HOLLERITH_COLUMNS = 80

# STARTX = 28 # for LATITUDE image
STARTX = 27
PITCHX = 582 / float(HOLLERITH_COLUMNS - 1)

# STARTY = 25 # for LATITUDE image
STARTY = 27
PITCHY = 240 / float(HOLLERITH_ROWS - 1)

LATITUDE_IMAGE = "latitude_95f9df43-b70c-49a0-ae72-2a1022699560_l.jpg"
LONGITUDE_IMAGE = "longitude_b81af7c3-b9cf-46f5-b283-3cdf15db0250_l.jpg"


def read_image(name):
    im = Image.open(name)
    color = (255, 0, 0)
    rowdata = []
    for col in range(HOLLERITH_COLUMNS):
        x = int(STARTX + PITCHX * col)
        coldata = []
        for row in range(HOLLERITH_ROWS):
            y = int(STARTY + PITCHY * row)
            coord = (x, y)
            coldata.append(im.getpixel(coord))
            im.putpixel(coord, color)
        rowdata.append(coldata)
    im.show()
    return rowdata

########################################################################

if __name__ == '__main__':

    import argparse
    import os
    import sys
    import textwrap
    import time
    import traceback

    def process():
        from pprint import pprint

    #   latdata = read_image(LATITUDE_IMAGE)
    #   pprint(latdata)
    #   return latdata

        londata = read_image(LONGITUDE_IMAGE)
        pprint(londata, width=24)
        return londata

#from pexpect import run, spawn

# Uncomment the following section if you want readline history support.
#import readline, atexit
#histfile = os.path.join(os.environ['HOME'], '.TODO_history')
#try:
#    readline.read_history_file(histfile)
#except IOError:
#    pass
#atexit.register(readline.write_history_file, histfile)

########################################################################

    global LONDATA

    def main():

        global OPTIONS
        global LONDATA

        LONDATA = process()

########################################################################

    try:
        START_TIME = time.time()

        PARSER = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage=textwrap.dedent(globals()['__doc__']),
            version="Version: %s" % __VERSION__
        )

        PARSER.add_argument(
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        OPTIONS = PARSER.parse_args()

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

    except KeyboardInterrupt as error_exception:        # Ctrl-C
        raise error_exception

    except SystemExit as error_exception:               # sys.exit()
        raise error_exception

    except Exception as error_exception:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(error_exception))
        traceback.print_exc()
        os._exit(1)

# end of file
