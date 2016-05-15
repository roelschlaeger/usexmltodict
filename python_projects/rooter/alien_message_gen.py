#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:nowrap
# $Id: alien_message_gen.py 197 2011-03-23 12:55:34Z harry $
# Timestamp: <timestamp>
########################################################################

"""Generate a puzzle like Alien Message #1."""

import sys

__author__ = "Robert L. Oelschlaeger"
__version__ = "$Revision: 198 $".split()[1]
__date__ = "$Date: 2016-05-15 15:51:34 -0500 (Sun, 15 May 2016) $".split()[1]

alphabet = {
    '0':   (' xxx ',
            'x   x',
            'x   x',
            'x   x',
            'x   x',
            'x   x',
            ' xxx ',
            ),

    '1':   ('  x  ',
            ' xx  ',
            '  x  ',
            '  x  ',
            '  x  ',
            '  x  ',
            'xxxxx',
            ),

    '2':   (' xxx ',
            'x   x',
            '   x ',
            '  x  ',
            ' x   ',
            'x    ',
            'xxxxx',
            ),

    '3':   (' xxx ',
            'x   x',
            '   x ',
            '  x  ',
            '   x ',
            'x   x',
            ' xxx ',
            ),

    '4':   ('   x ',
            '  xx ',
            ' x x ',
            'x  x ',
            'xxxxx',
            '   x ',
            '   x ',
            ),

    '5':   ('xxxx ',
            'x    ',
            'x    ',
            ' xxx ',
            '    x',
            'x   x',
            ' xxx ',
            ),

    '6':   ('  xx ',
            ' x   ',
            'x    ',
            'xxxx ',
            'x   x',
            'x   x',
            ' xxx ',
            ),

    '7':   ('xxxxx',
            'x   x',
            '   x ',
            '  x  ',
            ' x   ',
            'x    ',
            'x    ',
            ),

    '8':   (' xxx ',
            'x   x',
            ' x x ',
            '  x  ',
            ' x x ',
            'x   x',
            ' xxx ',
            ),

    '9':   (' xxx ',
            'x   x',
            'x   x',
            ' xxxx',
            '    x',
            '    x',
            ' xxx ',
            ),

    ' ':   ('     ',
            '     ',
            '     ',
            '     ',
            '     ',
            '     ',
            '     ',
            ),

    'N':   ('x   x',
            'x   x',
            'xx  x',
            'x x x',
            'x  xx',
            'x   x',
            'x   x',
            ),

    'W':   ('x   x',
            'x   x',
            'x   x',
            'x   x',
            'x x x',
            'xx xx',
            'x   x',
            ),

    '.':   ('     ',
            '     ',
            '     ',
            '     ',
            '     ',
            '  xx ',
            '  xx ',
            ),

    'o':   (' xxx ',
            ' x x ',
            ' xxx ',
            '     ',
            '     ',
            '     ',
            '     ',
            ),

    "'":   ('   x ',
            '  x  ',
            ' x   ',
            '     ',
            '     ',
            '     ',
            '     ',
            ),

}

########################################################################

DEFAULT_CHAR = '.'


def update(array, d, charnumber, row, col, c):
    """Compute and fill a location in array based on row, col."""
    loc = row * d + charnumber * 6 + col
    if array[loc] == DEFAULT_CHAR:
        array[loc] = c
    else:
        array[loc] = 'X'

########################################################################


def encode(s, array, c):
    """Encode the latitude/longitude string s into array."""
#   print "encode: %s" % s
    # check for, set up for latitude
    if c == 'N':
        d = 77
        ro = 0
        co = 0
    else:
        # et up for longitude
        d = 91
        ro = 4
        co = 20

    for charnumber, char in enumerate(s):
        # print "char: %s" % char
        f = alphabet[char]
        for row, l in enumerate(f):
            row += ro
#           print row, l
            for col, x in enumerate(l):
                col += co
#               print col, x,
                if x == 'x':
                    update(array, d, charnumber, row, col, c)

########################################################################


def main(args, options):
    """Run encoding from the console."""
    latitude = options.latitude
    longitude = options.longitude
    pitch = options.pitch

    if options.debug:
        for c in sorted(alphabet.keys()):
            print
            for l in alphabet[c]:
                print l

    array = [DEFAULT_CHAR] * 1001

    encode(latitude, array, 'N')
    encode(longitude, array, 'W')

    print
    x = array
    while x:
        s, x = x[:pitch], x[pitch:]
        print "".join(s)

########################################################################

if __name__ == "__main__":

    from optparse import OptionParser

    version = "%%prog - Version: %s, %s" % (__version__, __date__)
    usage = "%%prog - [options]"
    parser = OptionParser(usage=usage, version=version)

    parser.add_option(
        "-d", "--debug",
        action="count",
        dest="debug",
        help="Increment debug counter"
    )

    parser.add_option(
        "-p", "--pitch",
        action="store",
        dest="pitch",
        type="int",
        default=59,
        help="set pitch"
    )

    parser.add_option(
        "", "--latitude",
        action="store",
        dest="latitude",
        default="N38o50.599'",
        help="set latitude (default: %default)"
    )

    parser.add_option(
        "", "--longitude",
        action="store",
        dest="longitude",
        default="W090o17.953'",
        help="set longitude (default: %default)"
    )

    (options, args) = parser.parse_args()

    if args:
        parser.print_help()
        sys.exit(1)

    main(args, options)

########################################################################
