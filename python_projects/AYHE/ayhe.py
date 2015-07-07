#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Tue 07 Jul 2015 02:47:12 PM CDT
# Last Modified: Tue 07 Jul 2015 03:23:09 PM CDT

"""
SYNOPSIS

    ayhe [-h | --help] [-v | --version] [--verbose]

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

CENTER = "15S E 742748 N 4278287"
EASTINGS = int(CENTER.split()[2])
NORTHINGS = int(CENTER.split()[4])


def process():

    count = [0] * 6
    for A in range(10):
        count[0]+= 1
        if (A == 0):
            continue
        H = A
        for B in range(10):
            count[1]+= 1
            S = B
            for C in range(10):
                count[2]+= 1
                J = C - B
                if (J < 0):
                    continue
                Q = A - (B + C)
                if Q < 0:
                    continue
                K = B + C
                O = A + C
                for D in range(10):
                    count[3]+= 1
                    I = D / A
                    M = D - A
                    for E in range(10):
                        count[4]+= 1
                        P = E
                        G = E - B
                        if G < 0:
                            continue
                        L = D - E
                        if L < 0:
                            continue
                        for F in range(10):
                            count[5]+= 1
                            N = F - A
                            if N < 0:
                                continue
                            R = D - F
                            if R < 0:
                                continue
                            eastings = int(("%s" * 6) % (G, H, I, J, K, L))
                            if not(abs(eastings - EASTINGS) < 1609.34):
                                continue
                            northings = int(("%s" * 7) % (M, N, O, P, Q, R, S))
                            if not(abs(northings - NORTHINGS) < 1609.34):
                                continue
                            abcdef = ("%s" * 6) % (A, B, C, D, E, F)
                            print(
                                abcdef,
                                "15S" +
                                " E %06d" % eastings +
                                " N %07d" % northings
                            )
    print count

if __name__ == '__main__':

    import argparse
    import os
    import sys
    import textwrap
    import time
    import traceback

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
