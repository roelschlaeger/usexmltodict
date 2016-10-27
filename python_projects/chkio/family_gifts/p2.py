#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 27 Oct 2016 08:32:53 AM CDT
# Last Modified: Thu 27 Oct 2016 09:00:51 AM CDT

"""
SYNOPSIS

    TODO helloworld [-h | --help] [-v | --version] [--verbose]

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

from collections import defaultdict
from p0 import p0
from pprint import pprint

########################################################################


def edges(p1):
    return tuple(
        sorted(
            [
                (p1[i], p1[i + 1]) for i in range(len(p1) - 1)
            ] + [
                (p1[-1], p1[0])
            ]
        )
    )

########################################################################


def doit():
    def sub(p0, e0):
        print("e0", e0)
        groups = defaultdict(list)
        ungroups = defaultdict(list)
        for chain in p0:
            edge_group = edges(chain)
            if e0 in edge_group:
                groups[e0].append(chain)
            else:
                ungroups[e0].append(chain)
        pprint([(len(value), key) for key, value in groups.items()], width=240)
        pprint([(len(value), key) for key, value in ungroups.items()], width=240)
        return groups[e0]
    e0 = edges(p0[0])[0]
    p1 = sub(p0, e0)
    print()
    e1 = edges(p1[0])[1]
    p2 = sub(p1, e1)
    print()
    e2 = edges(p2[0])[2]
    p3 = sub(p2, e2)
    print()
    e3 = edges(p3[0])[3]
    p4 = sub(p3, e3)
    print()
    e4 = edges(p4[0])[4]
    p5 = sub(p4, e4)
    print()
    e5 = edges(p5[0])[5]
    p6 = sub(p5, e5)
    print()
    pprint(p5, width=240)
    print()
    pprint(p6, width=240)

########################################################################

if __name__ == '__main__':

    import argparse
    import os
    import sys
    import textwrap
    import time
    import traceback

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

        global OPTIONS

        doit()

########################################################################

    try:
        START_TIME = time.time()

        PARSER = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage=textwrap.dedent(globals()['__doc__']),
            version="Version: %s" % __VERSION__
        )

        PARSER.add_argument(
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        OPTIONS = PARSER.parse_args()

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
