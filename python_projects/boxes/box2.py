#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 03 Apr 2014 06:59:49 PM CDT
# Last Modified: Fri 04 Apr 2014 09:39:12 PM CDT

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

from itertools import permutations
from boxes import CUBES, SOLVERS
print "len(CUBES) = %d" % len(CUBES)
from pprint import pprint, pformat
from copy import deepcopy
import sys

########################################################################

NONE_LOCATIONS = []

########################################################################


def prep():
    print "prep"
    global NONE_LOCATIONS
    NONE_LOCATIONS = []
    for index, cube in enumerate(CUBES):
        print index, cube
        if cube is None:
            NONE_LOCATIONS.append(index)
    pprint(NONE_LOCATIONS)
    print "len(CUBES) = %d" % len(CUBES)

prep()
del prep

########################################################################


def fill_cubes(p):
#   print "fill_cubes"

#   cubes = CUBES

    # TODO: I don't know if deepcopy is required or not
    cubes = deepcopy(CUBES)

#   pprint(cubes, width=2)
#   print pformat(p), len(cubes), len(SOLVERS)

    for index, none_location in enumerate(NONE_LOCATIONS):
#       print none_location, index, p[index], SOLVERS[p[index]]
        assert cubes[none_location] is None, \
            ValueError("Unexpected cubes value at %d" % none_location)
        cubes[none_location] = SOLVERS[p[index]]

#   pprint(cubes)

    return cubes

########################################################################


def verify(cubes):

    # get the reference cube
    reference_cube = cubes[0]

    # check for missing
    if reference_cube is None:
        return False

    # check rest of cubes
    for comparision_cube in cubes[1:]:

        # not enough cubes?
        if comparision_cube is None:
            return False

        # get pattern, color, value
        p0, c0, v0 = reference_cube
        p1, c1, v1 = comparision_cube

        # check for one and only one difference
        if (p0 == p1) == (c0 == c1):
            return False

        # move the reference cube
        reference_cube = comparision_cube

    return True

if 0:
    print verify([("black", "black", "0"), ("black", "red", "1")])
    print verify([("black", "black", "0"), ("black", "black", "1")])
    print verify([("black", "black", "0"), ("red", "black", "1")])
    print verify([("black", "black", "0"), ("red", "red", "1")])
    print verify([("black", "black", "0")])
    print verify([
        ("black", "black", "0"),
        ("black", "red", "1"),
        ("blue", "red", "2")
    ])
    sys.exit()

# print "len(CUBES) = %d" % len(CUBES)
# print verify(CUBES)
# print "len(CUBES) = %d" % len(CUBES)

########################################################################


def my_print_cubes(cubes):

    for index, cube in enumerate(cubes):
        if cubes is None:
            cubes = ('?', '?', '?')
        p, c, v = cube
        print "%7s %6s %1s" % (p, c, v)
        if index == 7:
            print
    print

########################################################################


def job():

    print "job"

    skipping = [-1] * 5
    matching = [-1] * 5
    pprint(skipping)

    old_p2 = [-1] * 2

#   for p in permutations(range(10), 10):
    r = range(10)

    # give a head start to [7, 5, ...]
    if 0:
        r.remove(7)
        r.remove(5)
        r = [7, 5] + r

    for p in permutations(r, 10):

        if skipping == p[:5]:
#           print "Skipping: %s" % pformat(p)
            continue

        # use this for heartbeat output
        if old_p2 != p[:2]:
            print p
            old_p2 = p[:2]

        cubes = fill_cubes(p)

        # locate the first row candidate
        if not verify(cubes[:8]):
            continue

        # conditionally report a match if not reported before
        if matching != p[:5]:
            print "first row match: %s" % pformat(p[:5])
            my_print_cubes(cubes)
            # disable further matches of the first 5 solvers
            matching = p[:5]

        # now verify the back half of the array
        if verify(cubes[8:]):
            print "\tsecond row: %s" % pformat(p[5:])
            print p, pformat(cubes)

job()

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

        # TODO: Do something more interesting here...
        print 'Hello world!'

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
