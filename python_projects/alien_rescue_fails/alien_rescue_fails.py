#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Mon 25 Aug 2014 06:25:49 PM CDT
# Last Modified: Mon 25 Aug 2014 09:41:36 PM CDT

"""
SYNOPSIS

    TODO alien_rescue_fails [-h] [-v,--verbose] [--version]

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

__VERSION__ = "0.0.1"

########################################################################

from PIL import Image, ImageDraw

########################################################################


def draw_horizontals(im, minx, maxx, miny, maxy, dy):
    draw = ImageDraw.Draw(im)

    x0 = minx
    x1 = maxx
    y1 = miny

    while y1 < maxy:
        y0 = y1
        print x0, y0, x1, y1
        draw.line([(x0, y0), (x1, y1)], fill=128)
        y1 += dy

    del draw


def draw_verticals(im, minx, maxx, miny, maxy, dx):
    draw = ImageDraw.Draw(im)

#   x0 = minx
    x1 = minx
    y0 = miny
    y1 = maxy
    index = 0

    while x1 < maxx:
        width = 1
        if index % 8 == 0:
            width = 2
        x0 = x1
        print x0, y0, x1, y1
        draw.line([(x0, y0), (x1, y1)], fill=128, width=width)
        x1 += dx
        index += 1

    del draw


def process(filename):

    import os.path
    import sys

    outfilename, junk = os.path.splitext(filename)
    outfile = outfilename + "_out.jpg"

    im = Image.open(filename)
    print filename, im.format, im.size, im.mode, outfile

    minx = 24
    miny = 21
    dx = 9.4
    dy = 42.75
    maxy = im.size[1]
    maxx = im.size[0] - dx

    draw_horizontals(im, minx, maxx, miny, maxy, dy)
    draw_verticals(im, minx, maxx, miny, maxy, dx)

    im.save(outfile, "JPEG")

FILENAMES = [
    "s1.png",
    "s2.png",
    "s3.png",
    "s4.png",
]


def process_files():

    for filename in FILENAMES:
        process(filename)

########################################################################

if __name__ == '__main__':

    import sys
    import os
    import traceback
    import optparse
    import time

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

    def main():

        global options, args

        process_files()

########################################################################

    try:
        START_TIME = time.time()

        PARSER = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version=__VERSION__
        )

        PARSER.add_option(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        (OPTIONS, ARGS) = PARSER.parse_args()

        #   if len(ARGS) < 1:
        #       PARSER.error ('missing argument')

        if OPTIONS.verbose:
            print time.asctime()

        EXIT_CODE = main()

        if EXIT_CODE is None:
            EXIT_CODE = 0

        if OPTIONS.verbose:
            print time.asctime()
            print 'TOTAL TIME IN MINUTES:',
            print (time.time() - START_TIME) / 60.0

        sys.exit(EXIT_CODE)

    except KeyboardInterrupt, error_exception:        # Ctrl-C
        raise error_exception

    except SystemExit, error_exception:               # sys.exit()
        raise error_exception

    except Exception, error_exception:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(error_exception)
        traceback.print_exc()
        os._exit(1)

# end of file
