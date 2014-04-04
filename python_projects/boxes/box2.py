#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 03 Apr 2014 06:59:49 PM CDT
# Last Modified: Thu 03 Apr 2014 08:12:10 PM CDT

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

NONE_LOCATIONS = []


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


def fill_cubes(p):
#   print "fill_cubes"

#   cubes = CUBES

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


def verify(cubes):
#   cubes = deepcopy(cubes_in)
#   print "verify"
#   p0, c0, v0 = cubes.pop(0)

    cube0 = cubes[0]
    if cube0 is None:
        return False

    for index in range(1, len(cubes)):

        cube1 = cubes[index]

        if cube1 is None:
            return False

        p0, c0, v0 = cube0
        p1, c1, v1 = cube1

        if (p0 == p1) == (c0 == c1):
            return False

        cube0 = cube1

    return True

# print "len(CUBES) = %d" % len(CUBES)
# print verify(CUBES)
# print "len(CUBES) = %d" % len(CUBES)


def job():
    print "job"
    old_p2 = [-1, -1]
    for p in permutations(range(10), 10):
        if old_p2 != p[:2]:
            print p
            old_p2 = p[:2]

        cubes = fill_cubes(p)
        if verify(cubes):
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
