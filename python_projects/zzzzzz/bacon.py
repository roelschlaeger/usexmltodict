#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 28 Apr 2016 02:05:46 PM CDT
# Last Modified: Thu 28 Apr 2016 03:41:02 PM CDT

"""
SYNOPSIS

    bacon [-h | --help] [-v | --version] [--verbose] | [-r | --reverse]

DESCRIPTION

    Tests a Bacon cipher with all possible 5-character strings, optionally
    reversed. This Bacon cipher merges i/j and u/v; other codes are noted as
    errors.

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

__VERSION__ = "0.0.2"

########################################################################

####### "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
BACON = "ABCDEFGHIKLMNOPQRSTUWXYZ"


def bacon(slist, l, h, reverse=False):

    out = []
    for s in slist:

        # reverse the string?
        if reverse:
            s = "".join(reversed(list(s)))

        s = s.replace(l, "0")
        s = s.replace(h, "1")
        try:
            n = int(s, 2)
        except ValueError as e:
            print(e)
            n = 31
        if n < len(BACON):
            out.append(BACON[n])
        else:
            print("bacon: %s ? " % s)
            out.append('0b%s' % s)
    return out

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

    def test_bacon(reverse=False):
        import itertools
        ba = itertools.product("AB", repeat=5)
        sba = ["".join(s) for s in ba]
        result = bacon(sba, "A", "B", reverse)
        print(result)

########################################################################

    def main():

        global OPTIONS

        test_bacon(reverse=OPTIONS.reverse)

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
            help='reverse code string'
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
