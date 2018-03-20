#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:nowrap
# $Id: alien_message_gen.py 197 2011-03-23 12:55:34Z harry $
# Timestamp: <timestamp>
########################################################################

"""Generate a puzzle like Alien Message #1."""

import sys

assert sys.version_info > (3, ), "Python 3 required"

########################################################################

__VERSION__ = "0.0.199"
__DATE__ = "2017-07-29"

########################################################################

ALPHABET = {
    '0': (
        ' xxx ',
        'x   x',
        'x   x',
        'x   x',
        'x   x',
        'x   x',
        ' xxx ',
    ),

    '1':   (
        '  x  ',
        ' xx  ',
        '  x  ',
        '  x  ',
        '  x  ',
        '  x  ',
        'xxxxx',
    ),

    '2':   (
        ' xxx ',
        'x   x',
        '   x ',
        '  x  ',
        ' x   ',
        'x    ',
        'xxxxx',
    ),

    '3':   (
        ' xxx ',
        'x   x',
        '   x ',
        '  x  ',
        '   x ',
        'x   x',
        ' xxx ',
    ),

    '4':   (
        '   x ',
        '  xx ',
        ' x x ',
        'x  x ',
        'xxxxx',
        '   x ',
        '   x ',
    ),

    '5':   (
        'xxxx ',
        'x    ',
        'x    ',
        ' xxx ',
        '    x',
        'x   x',
        ' xxx ',
    ),

    '6':   (
        '  xx ',
        ' x   ',
        'x    ',
        'xxxx ',
        'x   x',
        'x   x',
        ' xxx ',
    ),

    '7':   (
        'xxxxx',
        'x   x',
        '   x ',
        '  x  ',
        ' x   ',
        'x    ',
        'x    ',
    ),

    '8':   (
        ' xxx ',
        'x   x',
        ' x x ',
        '  x  ',
        ' x x ',
        'x   x',
        ' xxx ',
    ),

    '9':   (
        ' xxx ',
        'x   x',
        'x   x',
        ' xxxx',
        '    x',
        '    x',
        ' xxx ',
    ),

    ' ':   (
        '     ',
        '     ',
        '     ',
        '     ',
        '     ',
        '     ',
        '     ',
    ),

    'N':   (
        'x   x',
        'x   x',
        'xx  x',
        'x x x',
        'x  xx',
        'x   x',
        'x   x',
    ),

    'W':   (
        'x   x',
        'x   x',
        'x   x',
        'x   x',
        'x x x',
        'xx xx',
        'x   x',
    ),

    '.':   (
        '     ',
        '     ',
        '     ',
        '     ',
        '     ',
        '  xx ',
        '  xx ',
    ),

    'o':   (
        ' xxx ',
        ' x x ',
        ' xxx ',
        '     ',
        '     ',
        '     ',
        '     ',
    ),

    "'":   (
        '   x ',
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


def update(array, _dimension, charnumber, row, col, _char):
    """Compute and fill a location in array based on row, col."""
    loc = row * _dimension + charnumber * 6 + col
    if array[loc] == DEFAULT_CHAR:
        array[loc] = _char
    else:
        array[loc] = 'X'

########################################################################


def encode(e_string, array, _char):
    """Encode the latitude/longitude string e_string into array."""
#   print "encode: %s" % e_string
    # check for, set up for latitude
    if _char == 'N':
        dimension = 77
        row_offset = 0
        col_offset = 0
    else:
        # set up for longitude
        dimension = 91
        row_offset = 4
        col_offset = 20

    for charnumber, char in enumerate(e_string):
        # print "char: %s" % char
        fontdata = ALPHABET[char]
        for row, leftover in enumerate(fontdata):
            row += row_offset
#           print row, leftover
            for col, xchar in enumerate(leftover):
                col += col_offset
#               print col, xchar,
                if xchar == 'x':
                    update(array, dimension, charnumber, row, col, _char)

########################################################################


def main(_args, options):
    """Run encoding from the console."""
    print(options)

    latitude = options.latitude
    longitude = options.longitude
    pitch = options.pitch

    if options.debug:
        for _char in sorted(ALPHABET.keys()):
            print()
            for leftover in ALPHABET[_char]:
                print(leftover)

    array = [DEFAULT_CHAR] * 1001

    encode(latitude, array, 'N')
    encode(longitude, array, 'W')

    print()
    xdata = array
    while xdata:
        sline, xdata = xdata[:pitch], xdata[pitch:]
        print("".join(sline))

########################################################################


if __name__ == "__main__":

    from argparse import ArgumentParser

    import textwrap
    PARSER = ArgumentParser(
        usage=textwrap.dedent(__doc__)
    )

    PARSER.add_argument(
        "-v",
        "--version",
        action="version",
        version="Version: %s %s" % (__VERSION__, __DATE__)
    )

    PARSER.add_argument(
        "-d", "--debug",
        action="count",
        dest="debug",
        help="Increment debug counter"
    )

    PARSER.add_argument(
        "-p", "--pitch",
        action="store",
        dest="pitch",
        type=int,
        default=59,
        help="set pitch"
    )

    PARSER.add_argument(
        "--latitude",
        action="store",
        dest="latitude",
        default="N38o50.599'",
        help="set latitude default: %(default)s"
    )

    PARSER.add_argument(
        "--longitude",
        action="store",
        dest="longitude",
        default="W090o17.953'",
        help="set longitude (default: %(default)s)"
    )

    OPTIONS = PARSER.parse_args()
    ARGS = None

    if ARGS:
        PARSER.print_help()
        sys.exit(1)

    main(ARGS, OPTIONS)

########################################################################
