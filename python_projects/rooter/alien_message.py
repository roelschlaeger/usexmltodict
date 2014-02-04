#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:nowrap
# $Id: alien_message.py 35 2008-07-17 05:34:05Z harry $
# Timestamp: <timestamp>
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

__author__  = "Robert L. Oelschlaeger"
__version__ = "$Revision: 35 $".split()[1]
__date__    = "$Date: 2008-07-17 00:34:05 -0500 (Thu, 17 Jul 2008) $".split()[1]

########################################################################

# 1001: 7 11 13

otext = """
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

text = """
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

text = """
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

from optparse import OptionParser
import sys

########################################################################

def print_t(t, i):
    """print i-length substrings of t, replacing 'W' or 'N' characters with '.'
depending on whether i is 77 or 91
@param t: the input
@type t: string
@param i: characters per line
@type i: integer"""

    o = []
    while t:
        h, t = t[:i], t[i:]
        if i == 77: h = h.replace("W", ".")
        if i == 91: h = h.replace("N", ".")
        o.append(h)
    print "\n".join(o)

########################################################################

def main(args, options):
    """reformat 'text' to generate the latitude and longitude of the cache"""

    t = "".join(text.split("\n"))
    print len(t)

#   for i in [ 7, 11, 13, 77, 91, 143 ]:
    for i in [ 77, 91, ]:
        print i
        print
        print_t(t, i)

########################################################################

if __name__=="__main__":

    from optparse import OptionParser

    version = "%%prog - Version: %s, %s" % (__version__, __date__)
    usage = "%%prog - [options]"
    parser = OptionParser(usage=usage, version=version)

    parser.add_option("-d", "--debug",
        action="count",
        dest="debug",
        help="Increment debug counter")

    (options, args) = parser.parse_args()

    if args:
        parser.print_help()
        sys.exit(1)

    main(args, options)

########################################################################
