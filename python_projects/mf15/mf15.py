#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 17 Apr 2014 04:15:58 PM CDT
# Last Modified: Fri 18 Apr 2014 08:22:03 PM CDT

"""
SYNOPSIS

    TODO helloworld [-h] [-v,--verbose] [--version]

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

from pprint import pprint, pformat

########################################################################

TOKENS = "123456789ABCDEFG"

TABLEAU = """
.5a.g......7.8d.
...f28....dc4...
...8..1a69..c...
gd.c........5.26
82.d9.6..b.1e.a3
..9b..3..5..6c..
6.5..........b.7
7f...2.4c.9...18
3e...f.69.1...5b
a.d..........6.e
..f6..9..a..14..
cg.14.e..f.d7.89
f3.a........d.g4
...e..gf17..9...
...g83....fea...
.7b.1......5.f6.
"""
TABLEAU = TABLEAU.upper()
TABLEAU = TABLEAU.replace('.', ' ')

########################################################################

########################################################################


def compute_rows(tableau_rows):

    tokens = set(list(TOKENS))

    result = []
    for row in tableau_rows:
        inrow = set(list(row))
        diff = tokens - inrow
        result.append(diff)

    return result

########################################################################


def transpose(t):

    columns = []

    for index in range(len(t[0])):
        s = ""
        for row in range(len(t)):
            s += t[row][index]
        columns.append(s)

    return columns

########################################################################


def compute_columns(tableau_rows):
    tableau_columns = transpose(tableau_rows)
    return compute_rows(tableau_columns)

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

        tableau_rows = TABLEAU.split("\n")[1:-1]
        pprint(tableau_rows)

        def alter(r, c, v):
            print "alter: %d %d %s" % (r, c, v)
            row = tableau_rows[r]
            print r, c, v, row
            row = list(row)
            pprint(row)
            assert row[c] == " ", \
                IndexError("Invalid alteration: %s" % row[c], v)
            row[c] = v
            tableau_rows[r] = "".join(row)

        alter(1, 13, '9')
#       alter(2, 1, 'B')
#       alter(7, 3, '3')
#       alter(7, 12, 'B')
#       alter(10, 1, '8')
#       alter(0, 3, '9')
#       alter(6, 3, '2')
#       alter(15, 3, '4')
#       alter(8, 3, '7')
#       alter(9, 3, '5')
        pprint(tableau_rows)

        rows = compute_rows(tableau_rows)
        pprint(rows)

        columns = compute_columns(tableau_rows)
        pprint(columns)

        dresult = {}
        for irow, row in enumerate(rows):
            tr = tableau_rows[irow]
            print irow, pformat(row)
            for icolumn, column in enumerate(columns):
                tc = tr[icolumn]
                if tc == " ":
                    both = row.intersection(column)
                    print "##%2d %2d %2d %s" % (len(both), irow, icolumn, both)
                    dresult[(irow, icolumn)] = both
            print

        def select(r, c):
            t = (r, c)
            both = dresult.get(t, None)
            if both is None:
                both = "Get from original"
            print "%2d %2d %s" % (r, c, pformat(both))

        print "latitude"
        select(1, 13)
        select(2, 13)
        select(3, 2)
        select(9, 3)
        select(12, 2)
        select(12, 8)
        select(13, 14)

        print "longitude"
        select(1, 5)
        select(2, 0)
        select(2, 10)
        select(7, 15)
        select(8, 2)
        select(8, 3)
        select(14, 15)

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
