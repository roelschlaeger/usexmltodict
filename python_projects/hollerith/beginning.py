#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Mon 02 May 2016 03:15:43 PM CDT
# Last Modified: Tue 03 May 2016 06:57:49 PM CDT

"""
SYNOPSIS

    beginning [-h | --help] [-v | --version] [--verbose]

DESCRIPTION

    Processing for "In the beginning..." GC?????
    This script processes data extracted from a Hollerith card.

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

########################################################################

from hollerith import HOLLERITH

LATITUDE = """
Y6
X6
X9

Y6
Y9
X5
Y1
X3

X3
X6
Y3
Y1
03
Y9
X6
X5

X9
Y5
X7
X3
Y1
Y3
Y5

X5

Y4
Y5
Y3

X4
Y9
X5
04
03
Y5
02

06
Y9
03
Y8

Y5
Y9
Y7
Y8
03

Y8
04
X5
Y4
X9
Y5
Y4

Y6
X6
04
X9
03
08

03
06
X6

Y1
X5
Y4






"""


LONGITUDE = """

Y4
Y4

X6
X5
Y5

Y8
04
X5
Y4
X9
Y5
Y4

03
06
Y5
X3
05
Y5

03
X6

03
Y8
Y5

06
Y5
02
03

Y4
Y5
Y3
Y9
X4
Y1
X3

X4
Y9
X5

03
Y5




X5
X6
06


Y9
X5
Y4

03
Y8
Y5

Y3













"""

from both_txt import *


def decode(strings):
    out = []

    for s in strings:
        if s in HOLLERITH:
            out.append(HOLLERITH[s])
        else:
            out.append(" ")
    return "".join(out)


def decode_strings(s):
    strings = s.split("\n")[1:-1]
    return decode(strings)


def process():
#   print("latitude")
    print(decode_strings(LATITUDE))
#   print()
#   print("longitude")
    print(decode_strings(LONGITUDE))


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

        process()

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
