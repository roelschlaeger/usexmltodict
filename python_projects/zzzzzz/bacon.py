#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 28 Apr 2016 02:05:46 PM CDT
# Last Modified: Thu 28 Apr 2016 02:21:43 PM CDT

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

####### "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
BACON = "ABCDEFGHIKLMNOPQRSTUWXYZ"


def bacon(slist, l, h):
    out = []
    for s in slist:
        s = s.replace(l, "0")
        s = s.replace(h, "1")
        n = int(s, 2)
        if n < len(BACON):
            out.append(BACON[n])
        else:
            out.append(" %s ? " % s)
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

    def test_bacon():
        result = bacon(
            [
                "AAAAA",
                "AAAAB",
                "AAABA",
                "AAABB",
                "AABAA",
                "AABAB",
                "AABBA",
                "AABBB",
                "ABAAA",
                "ABAAB",
                "ABABA",
                "ABABB",
                "ABBAA",
                "ABBAB",
                "ABBBA",
                "ABBBB",
                "BAAAA",
                "BAAAB",
                "BAABA",
                "BAABB",
                "BABAA",
                "BABAB",
                "BABBA",
                "BABBB",
            ],
            "A",
            "B")

        print(result)

########################################################################

    def main():

        global OPTIONS

        test_bacon()

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
