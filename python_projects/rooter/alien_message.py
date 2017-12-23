#!/usr/bin/env python
# coding=utf-8

########################################################################

"""Decrypt the hint message for
U{Alien Message #1 MO<http://www.geocaching.com/seek/cache_details.aspx?guid=25e0659c-6f7d-4e51-8f23-79a043d5f8b6>}
GC19B71

The key to the solution is that the input text contains exactly 1001
characters, which has three prime factors: 7, 11, and 13. Formatting the
encoded text as 7x11=77 characters per line yields a block-letter
representation of the latitude, formatting it as 7x13=91 characters per line
yields the longitude.

Four characters are used in the encoding:

    -   '.' to represent a blank
    -   'N' to represent a latitude pixel
    -   'W' to represent a longitude pixel
    -   'X' to represent both a latitude and longitude pixel

When printing the latitude, 'W' characters are ignored by converting them to
'.'; when printing the longitude, 'N' characters are ignored by converting them
to '.'.

Here is sample output::

    1001
    77

    .NNN......NN......NNN...N.......NNN....NNN...N...............................
    N...N....N.N.....N...N..N......N...N..N...N..N...............................
    ....N...N..N.....N...N..N......N..........N..N...............................
    ..NN...N...N.....N...N..N......NNNN.....NN...N...............................
    ....N..NNNNN.....N...N..N......N...N......N..N...............................
    N...N......N.....N...N..X..NX..N...X..N...N..X...............................
    .NNN.......N......NNN...N..NN...NNN....XNN...N...............................
    .............................................................................
    .............................................................................
    .............................................................................
    .............................................................................
    .............................................................................
    .............................................................................
    91

    ...........................................................................................
    ...........................................................................................
    ...........................................................................................
    ...........................................................................................
    ...........................................WWX...X......XWW......WX......W...WWW....WWW....
    ..........................................W...X..W.....W...W....W.W......W..W...W..W...W...
    ..........................................W...W..W.....W...W...W..W......W..W...W..W.......
    ...........................................WWW...W.....W...W..W...W......W..W...W..WWWW....
    ..........................................W...W..W.....W...W..WWWWW......W..W...W..W...W...
    ..........................................W...W..W.....W...W......W..WW..W..W...W..W...W...
    ...........................................WWW...W......WWW.......W..WW..W...WWW....WWW....

"""

########################################################################

import sys

assert sys.version_info > (3, ), "Python 3 required"

########################################################################

# __author__ = "Robert L. Oelschlaeger"
# __version__ = "$Revision: 35 $".split()[1]
# __date__ = "$Date: 2008-07-17 00:34:05 -0500 (Thu, 17 Jul 2008) $".split()[1]

__VERSION__ = "0.0.36"
__DATE__ = "2017-07-29"

########################################################################

# 1001: 7 11 13

OTEXT = """
.NNN......NN......NNN...N.......NNN....NNN...N.............
..................N...N....N.N.....N...N..N......N...N..N..
.N..N...................................N...N..N.....N...N.
.N......N..........N..N.................................NN.
..N...N.....N...N..N......NNNN.....NN...N..................
.................N..NNNNN.....N...N..N......N...N......N..N
...............................N...N......N.....N...NWWX..N
X..N...XWWN...N.WX......W...WWW....WWW............NNN......
.N......NNN...N..NN...NNNW...XNNW..N..W...W....W.W......W..
W...W..W...W.............................................W.
..W..W.....W...W...W..W......W..W...W..W...................
...............................WWW...W.....W...W..W...W....
..W..W...W..WWWW...........................................
...W...W..W.....W...W..WWWWW......W..W...W..W...W..........
...................................W...W..W.....W...W......
W..WW..W..W...W..W...W.....................................
.........WWW...W......WWW.......W..WW..W...WWW....WWW....
"""
"""This was the text string for the original cache"""

TEXT = """
N...N..NNN...NNN...NNN..NNNN...NNN........NNNN...NNN.....N.
....N.............N...N.N...N.N...N..N.N..N.....N...N......
.N.....N...N...NN....N..............NN..N....N...N.N...NNN.
.N.....N...N.......N.....N...N..N.N...N...............N.N.N
...N.....N..........NNN..N...N........NNN...NNNN.N..N......
.............N..NN....N...N.N............N.N...N...........
N.....N.NNNNN.................WN..WN.XWW.N.XWW.N.WWW...XWW.
N.NW..NWWWXX..N...N.WWW.NWWWWN..WWW.....W........N...N..NNN
...XNN.W.W...W.XNN.W.XNN.W..XNW..NXX...XNN.W...N...W...W.W.
....W...W...W......................W...W.W...W.W...W.W...W.
.WWW....W......W........W...W.W.....W...W..W...............
........W...W.W...W..WWWW.W...W.........W.....W..........WW
WW..WWW...WWWW..........................W.W.W.W...W.....W.W
...W.........W....W..............W.....W.....W.............
.............WW.WW.W...W.....W.W...W.........W...W.......WW
......W.W...W.....W..........................W...W..WWW...W
WW...WWW........WWWWW.W.......WW...WWW...WWW...WWW.......
"""

TEXT = """
N...N..NNN...NNN...NNN..NNNN...NNN........NNNN...NNN...NNN.
....N.............N...N.N...N.N...N..N.N..N.....N...N......
.N.....N...N.N...N...N..............NN..N....N...N.N...NNN.
.N.....N...N.......N.....N...N.N...N..N...............N.N.N
...N.....N..........NNN..N...N........NNN...NNNN..NNNN.....
.............N..NN....N...N.N............N.N...N...........
N.....N.....N.................WN..WN.XWW.N.XWW.N.WWW...XWW.
N.NW..NWWWXX..N...N.WWW.NWWWW.N.WWW.....W........N...N..NNN
...XNN.W.W...W.XNN.W.XNN.W..XNW..NXX...XNN.W.NNN...W...W.W.
....W...W...W......................W...W.W...W.W...W.W...W.
.WWW....W......W........W...W.W........W...W...............
........W...W.W...W..WWWW.W...W.........W.....W..........WW
WW..WWW....W............................W.W.W.W...W.....W.W
...W.........W....W..............W.....W....W..............
.............WW.WW.W...W.....W.W...W.........W...W.......WW
......W.W...W.W...W..........................W...W..WWW...W
WW...WWW........WWWWW.W.......WW...WWW...WWW...WWW.......
"""
"""this is the encoded text string for my cache"""

########################################################################


def print_t(_tail, i):
    """print i-length substrings of _tail, replacing 'W' or 'N' characters with '.'
depending on whether i is 77 or 91
@param _tail: the input
@type _tail: string
@param i: characters per line
@type i: integer"""

    _output = []
    while _tail:
        _head, _tail = _tail[:i], _tail[i:]
        if i == 77:
            _head = _head.replace("W", ".")
        if i == 91:
            _head = _head.replace("N", ".")
        _output.append(_head)
    print("\n".join(_output))

########################################################################


def main(_args, _options):
    """reformat 'text' to generate the latitude and longitude of the cache"""

    _t = "".join(TEXT.split("\n"))
    print(len(_t))

#   for i in [ 7, 11, 13, 77, 91, 143 ]:
    for i in [77, 91]:
        print(i)
        print()
        print_t(_t, i)

########################################################################


if __name__ == "__main__":

    from argparse import ArgumentParser

    VERSION = "%%(prog)s - Version: %s, %s" % (__VERSION__, __DATE__)
    USAGE = "%%(prog)s - [options]"

    import textwrap
    PARSER = ArgumentParser(usage=textwrap.dedent(__doc__))
    PARSER.add_argument(
        "-d",
        "--debug",
        action="count",
        dest="debug",
        help="Increment debug counter"
        )

    PARSER.add_argument(
        "--version",
        action="version",
        version=VERSION
        )

    OPTIONS = PARSER.parse_args()

    main(None, OPTIONS)

########################################################################
