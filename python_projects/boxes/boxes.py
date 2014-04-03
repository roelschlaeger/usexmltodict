#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 02 Apr 2014 03:28:01 PM CDT
# Last Modified: Thu 03 Apr 2014 01:13:59 PM CDT

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

PATTERNS = ["green", "blue", "square", "pattern", "black"]

COLORS = ["black", "red", "yellow", "white"]

CUBES = [
    ("green",   "black",  "N"),
    None,
    ("green",   "red",    "8"),
    None,
    ("blue",    "yellow", "9"),
    None,
    None,
    None,
    ("square",  "black",  "W"),
    None,
    ("pattern", "black",  "5"),
    None,
    ("green",   "red",    "9"),
    None,
    None,
    None,
]

SOLVERS = [
    ("square",  "yellow", "2"),
    ("black",   "white",  "0"),
    ("black",   "red",    "5"),
    ("pattern", "white",  "0"),
    ("black",   "black",  "9"),
    ("blue",    "red",    "5"),
    ("pattern", "red",    "3"),
    ("green",   "white",  "3"),
    ("green",   "red",    "6"),
    ("green",   "yellow", "3"),
]


def verify(cubes):
    print "verifying"
    for cube in cubes:
        if cube is None:
            continue
        else:
            p, c, v = cube
            assert p in PATTERNS, "%s is not in PATTERNS" % p
            assert c in COLORS, "%s is not in COLORS" % c


def print_cubes(cubes, solvers, index, index2):

    print '==='
    print index, pformat(cubes, width=1024)
    print index2, solvers[index2][2], pformat(solvers, width=1024)

    out = []
    for cube in cubes:
        if cube is None:
            out.append("?")
        else:
            out.append(cube[2])
    print
    print "".join(out)
    print

# verify(CUBES)
# verify(SOLVERS)


def solve(cubes, solvers):

#   states = []

    for index, cube in enumerate(cubes):

        # find a cube needing replacement
        if cube is None:

            # get previous pattern, color and value
            p0, c0, v0 = cubes[index - 1]

            # look for a solver
            for index2, solver in enumerate(solvers):

                # no match
                if solver is None:
                    continue

                p1, c1, v1 = solver

                # check for pattern or color match
                if (
                    (p0 == p1) and (not (c0 == c1))
                ) or (
                    (not (p0 == p1)) and (c0 == c1)
                ):

                    # check for following cube, if any
                    next = index + 1

                    if next < len(cubes):

                        if cubes[next] is not None:

                            p2, c2, v2 = cubes[next]

                            # check for possible pattern or color match
                            if not ((
                                (p1 == p2) and (not (c1 == c2))
                            ) or (
                                (not (p1 == p2)) and (c1 == c2)
                            )):
                                continue

                    # show status
                    print_cubes(cubes, solvers, index, index2)

                    # install the solver into the answer
                    cubes[index] = solver
                    solvers[index2] = None

                    # solve the rest
                    solve(cubes, solvers)

                    # restore the previous state
                    cubes[index] = CUBES[index]
                    solvers[index2] = solver

            for cube in cubes:
                if cube is None:
                    return

    print '---'
    pprint(cubes, width=1024)

solve(CUBES, SOLVERS)

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
