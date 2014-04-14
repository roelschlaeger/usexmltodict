#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Mon 14 Apr 2014 05:41:26 PM CDT
# Last Modified: Mon 14 Apr 2014 06:11:19 PM CDT

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

SOLUTION = """
69688 9875 9600
23587 2039 2220
62264 6311 6824
9061   40157695
   1542 888 938
03722431 899
518 18317 69786
9949 67121 8380
66398 29885 694
   472 90156203
461 051 8537
69789046   0385
7701 3331 19688
7516 8778 26130
8328 6297 78948
"""

LOCATIONS = [
    ('K', (0, 1, 3)),
    ('E', (1, 0, 0)),
    ('L', (1, 2, 2)),
    ('D', (3, 0, 1)),
    ('M', (3, 1, 3)),
    ('J', (4, 0, 1)),
    ('N', (6, 0, 0)),
    ('F', (7, 2, 1)),
    ('G', (8, 0, 4)),
    ('B', (8, 1, 1)),
    ('C', (9, 1, 3)),
    ('H', (11, 0, 3)),
    ('A', (12, 1, 2)),
    ('I', (14, 0, 0))
]
"""Locations of the answer digits within SOLUTION"""

DIGITS = {
    3: [
        51, 127, 187, 461, 472, 518, 521, 553, 694, 874, 888, 899, 926, 938,
        994, 998
    ],
    4: [
        385, 596, 1542, 1815, 2039, 2220, 3196, 3331, 3619, 4486, 5808, 5896,
        6043, 6269, 6297, 6311, 6379, 6526, 6824, 7362, 7516, 7701, 7843, 8034,
        8168, 8328, 8380, 8537, 8709, 8778, 8834, 8890, 9061, 9267, 9320, 9600,
        9875, 9949
    ],
    5: [
        458, 2293, 11199, 14372, 17012, 18317, 19688, 23372, 23587, 26130,
        29885, 46778, 62264, 62869, 66398, 67121, 69688, 69735, 69786, 72808,
        73108, 78948
    ],
    6: [
        250386, 591188, 670968, 886112
    ],
    8: [
        3722431, 40157695, 69789046, 90156203
    ]
}

########################################################################


def show_result():

    # extract interesting lines only
    solution = SOLUTION.split('\n')[1:-1]

#   for index, line in enumerate(solution):
#       print index, line
#   print

    # empty the output list
    out = []

    # locate result characters
    for loc in sorted(LOCATIONS):
#       pprint(loc)
        a, rcl = loc
#       pprint(rcl)
        row, col, ch = rcl
#       print solution[row]
        words = solution[row].split()
#       print a, row, col, ch, words[col][ch]
        out.append(words[col][ch])

    # reformat the output by inserting formatting
    out.insert(0, 'N')
    out.insert(3, ' ')
    out.insert(6, '.')

    out.insert(10, ' ')
    out.insert(11, 'W')
    out.insert(14, ' ')
    out.insert(17, '.')

    print "".join(out)

########################################################################


def parse():
    lines = SOLUTION.split('\n')[1:-1]
#   print len(lines)
#   print
    print "\n".join(lines)
    print
#   pprint(SOLUTION)
#   print

    for line in lines:
        words = line.split()
        for word in words:
            n = int(word)
            l = len(word)
            assert n in DIGITS[l], \
                IndexError("Can't find %d in %s" % (n, pformat(DIGITS[l])))

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

        parse()
        show_result()

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
