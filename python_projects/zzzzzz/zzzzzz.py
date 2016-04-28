#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 27 Apr 2016 08:03:11 AM CDT
# Last Modified: Thu 28 Apr 2016 03:44:55 PM CDT

"""
SYNOPSIS

    TODO helloworld [-h | --help] [-v | --version] [--verbose]

DESCRIPTION

    Solve the puzzle presented in GC1zzzz (http://coord.info/gc1zzzz)

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

from __future__ import print_function

__VERSION__ = "0.0.1"

ZZZ = """
ZZzZZzZZzzZZzZzZZzZzzZ
ZzZzZzzZZzZzZzzZZz
ZzzZZzzZzZzZzZ
ZzZzZzzZZzZzzZ
ZZzZzZzzZzzZzZZzZ
ZZzZZzZzzZzZzzZ
ZzZzZzZzzZZzZzzZ
ZZzZzZzzZZzZzzZzZzZZ
ZzZzZzzZzzZZ
ZzZzZzZZzzZzzZzZzZ
ZZzZZzzZZzZZzZZzzZzZZzZ
ZzZzZZzzZZzZzzZzZ
ZzzZzzZzZZzZ
ZzzZZzZZzZzZzzZzZzZ
ZZzzZzZzZzZzzZZzZZzZ
ZZzZZzZzzZzzZZzZzZ
ZZzzZzZzZzZzzZZzZZzZ
ZzZzzZzzZZzZzZZzZZ
ZzZzZzzZzzZzZZzZZ
ZzZzzZzzZZ
--------------------
ZZzZZzZZzzZZzZzZZzZzzZ
ZzZzZzzZZzZzZzzZZzZ
ZzZzZzZZzzZzzZzZzZ
ZzZzZzzZZzZzzZ
ZzzZzZZzZZzzZZ
ZZzZzZZzZZzzZZzzZZzZ
ZZzZzZzzZZzZzzZzZzZZ
ZZzZzZzzZzzZzZZzZ
ZZzZZzZzzZzZzzZ
ZzZzZzZzzZZzzZzZzZzZ
ZzZzZZzzZZzZzzZzZ
ZzZzZzzZzzZZ
ZZzZZzZZzzZZzZzZZzZZzzZZ
ZZzZZzzZzzZZzZ
ZZzzZzZzZzzZ
ZzZZzZzzZzZzzZzZzZzZ
ZzzZZzZzZzzZ
ZzzZzZZzZzzZZzZZzZ
ZZzzZzZZzZzzZZzZZzZZ
ZZzZzzZZzZZzZZzzZZzZzZZzZZ
ZzZZzZzzZZzZZzZZzzZZzZ
ZzZzZZzZzzZzZzZzZzzZZ
ZzzZZzzZzZZ
ZZzzZzZZzzZZzZzZ
ZzZzZzzZzZzzZ
ZZzZzZZzZzzZZzZZzZZzzZzZZzZzZ
ZZzZzZZzZzzZzzZzZzZzZ
ZzZzZzZzzZZzZzZZzZzzZzZZ
ZZ
"""

########################################################################


def split_by_blocks(s, l):
    out = []
    while s:
        t, s = s[:l], s[l:]
        out.append(t)
    return out

########################################################################


def print_by_blocks(s, l):
    print("print_by_blocks: %d" % l)
    while s:
        t, s = s[:l], s[l:]
        print(t)
    print()

########################################################################

# from pprint import pprint
from bacon import bacon


def process(reverse):
    zzz = ZZZ.split("\n")[1:-1]
    allz = "".join(zzz)
#   allz = "".join(reversed(list(allz)))
#   pprint(allz)
#   allz = "".join(allz)
    bb = split_by_blocks(allz, 5)
    print(bacon(bb, "Z", "z", reverse=reverse))

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

        process(OPTIONS.reverse)

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

        PARSER.add_argument(
            '-r',
            '--reverse',
            action='store_true',
            default=False,
            help='reverse strings to bacon()'
        )

        OPTIONS = PARSER.parse_args()

        if OPTIONS.verbose:
            print(time.asctime())

        EXIT_CODE = main()

        if EXIT_CODE is None:
            EXIT_CODE = 0

        if OPTIONS.verbose:
            print(time.asctime())
            print('TOTAL TIME IN MINUTES:',)
            print((time.time() - START_TIME) / 60.0)

        sys.exit(EXIT_CODE)

    except KeyboardInterrupt as error_exception:        # Ctrl-C
        raise error_exception

    except SystemExit as error_exception:               # sys.exit()
        raise error_exception

    except Exception as error_exception:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(error_exception))
        traceback.print_exc()
        os._exit(1)

# end of file
