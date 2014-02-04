#!/usr/bin/python
# vim:ts=4:sw=4:tw=0:wm=0:et
# $Id: $
# Created: 	     Mon 03 Oct 2011 10:52:15 AM CDT
# Last modified: Tue 04 Feb 2014 03:00:06 PM CST

########################################################################

"""Use the Franklin Order 8 Magic Square for encryption

http://www.mathpages.com/HOME/kmath155.htm
"""

__version__ = "$Revision: $".split()[1]
__date__ = "$Date: $".split()[1]

########################################################################

from pprint import pprint

########################################################################

DEBUG = False

########################################################################

FRANKLIN = """\
52 61  4 13 20 29 36 45
14  3 62 51 46 35 30 19
53 60  5 12 21 28 37 44
11  6 59 54 43 38 27 22
55 58  7 10 23 26 39 42
 9  8 57 56 41 40 25 24
50 63  2 15 18 31 34 47
16  1 64 49 48 33 32 17
"""

########################################################################

if __name__ == "__main__":

    ########################################################################

    def build_dictionaries():

        d = {}
        dr = {}

        for row_number, row in enumerate(FRANKLIN.split('\n')):

            for col_number, digits in enumerate(row.split()):

                if DEBUG:
                    print "%02d %02d %2s" % (row_number, col_number, digits)

                t = (row_number, col_number)
                n = int(digits)
                d[t] = n
                dr[n] = t

            if DEBUG:
                print

        return d, dr

    ########################################################################

    def decode(s, d):

        s = s.upper()

        result = list("_" * 64)

        for row in range(8):
            for col in range(8):
                t = (row, col)
                index = d[t]
                result[index - 1] = s[row * 8 + col]

        return "".join(result)

    ########################################################################

    def encode(s, dr):

        s = s.upper()

        if DEBUG:
            print s

        o = []
        for row in range(8):
            r = []
            for col in range(8):
                r.append("")
            o.append(r)

        for index, c in enumerate(s):

            row, col = dr[index + 1]
            o[row][col] = c

        if DEBUG:
            pprint(o)

        return "\n".join(["".join(r) for r in o])

    ########################################################################

    def main(args, options):
        """process each of the command line arguments"""

        d, dr = build_dictionaries()
        if DEBUG:
            pprint(dr)

        for arg in args:

            s = arg.replace(' ', '')
            s += 'X' * (64 - len(s))
            assert len(s) == 64

            if DEBUG:
                print s

            if not options.encode:
                result = decode(s, d)
            else:
                result = encode(s, dr)

            print "".join(result.split('\n'))
            print

    ########################################################################

    from optparse import OptionParser
#   import sys

    USAGE = "%prog { options }"
    VERSION = "Version: %(version)s, %(date)s" % {
        "version":   __version__,
        "date":   __date__,
    }

    PARSER = OptionParser(usage=USAGE, version=VERSION)

    PARSER.add_option("-d",
                      "--debug",
                      dest="debug",
                      action="count",
                      help="increment debug counter")

    PARSER.add_option("-e",
                      "--encode",
                      dest="encode",
                      action="store_true",
                      help="encode")

    (OPTIONS, ARGS) = PARSER.parse_args()

    if not ARGS:
        ARGS = [
            "norththirtyeightdegreesfiftysixpointeighteighteightminutes",
            "westninetydegreesfiftyeightpointthreethreethreeminutes",
            "MXTIRSTHGRXTTNIGIXHEEYEGYTXNIITEUSHTSFGERIETTHIFHXOHEXIETNXGIOPD",
            "TXTGFOERRSXUERIIEXNETPEHDIXSTTTYXXNYEHHETEXXERGINXEEFNHEEWXIMTTS",
        ]

    main(ARGS, OPTIONS)

########################################################################
