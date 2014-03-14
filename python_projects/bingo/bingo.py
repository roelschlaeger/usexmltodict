#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Fri 14 Mar 2014 09:52:02 AM CDT
# Last Modified: Fri 14 Mar 2014 12:45:56 PM CDT

"""
SYNOPSIS

    bingo.py [-h] [-v,--verbose] [--version]

DESCRIPTION

    Compute checksums for "Rest Stop BINGO"

    http://www.geocaching.com/
    geocache/
    GC4YPE2_rest-stop-bingo?guid=1b22b3c1-fc9f-4824-ac92-af4de6f9a395

EXAMPLES

    python bingo.py bingo.txt

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Robert Oelschlaeger <roelschlaeger@gmail.com>

LICENSE

    This script is in the public domain.

"""

__VERSION__ = "1.0.0"

########################################################################

from pprint import pformat, pprint
from collections import defaultdict

########################################################################

SIGNS = [
    #   """ONE""",
    #   """TWO""",
    #   """THREE""",
    #   """FOUR""",
    #   """FIVE""",
    #   """SIX""",
    #   """SEVEN""",
    #   """EIGHT""",
    #   """NINE""",
    #   """TEN""",
    #   """ELEVEN""",
    #   """TWELVE""",
    #   """THIRTEEN""",
    #   """FOURTEEN""",
]

CHECKSUMS = [
    8,
    118,
    5,
    7,
    87,
    14,
    3,
    5,
    2,
    0,
    39,
    7,
    4,
    13,
]

EQUATIONS = [
    lambda B, I, N, G, O: (B + I + N + G) / O,                  # Sign 1
    lambda B, I, N, G, O: (B - I + N + O - G) / 5,              # Sign 2
    lambda B, I, N, G, O: (B + I + N + G + O) / 5,              # Sign 3
    lambda B, I, N, G, O: (B + I) + (N * O) - G,                # Sign 4
    lambda B, I, N, G, O: ((O - N) + (I / B) + G) / 2,          # Sign 5
    lambda B, I, N, G, O: ((N + O) / G) + (B * I),              # Sign 6
    lambda B, I, N, G, O: (B + I + N + G + O) * 2,              # Sign 7
    lambda B, I, N, G, O: ((B + I + N + G) * O) + 3,            # Sign 8
    lambda B, I, N, G, O: (B + I + N + G + O) / O,              # Sign 9
    lambda B, I, N, G, O: (B * I) + ((N - G) * O),              # Sign 10
    lambda B, I, N, G, O: (O - B - G) - (N - I),                # Sign 11
    lambda B, I, N, G, O: I + (B * N * G * O),                  # Sign 12
    lambda B, I, N, G, O: (B + I + G) + (N * N) + O,            # Sign 13
    lambda B, I, N, G, O: (I + N) + (B * G * O),                # Sign 14
]

EQUATIONS_CHECKSUM = 67

########################################################################


def compute_sign_values(s, equation):
    """Count 'B', 'I', 'N', 'G', and 'O' characters in #{s}
"""

    s = s.upper()
    d = defaultdict(lambda: 0)

    # count the letters
    for c in s:
        d[c] += 1

    # collect the results
    result_list = []
    checksum = 0
    for c in "BINGO":
        value = d[c]
        checksum += value
        result_list.append(value)

    result_tuple = tuple(result_list)

    try:
        equation_result = equation(*result_tuple)
    except ZeroDivisionError:
        equation_result = 99999999

    return checksum, result_tuple, equation_result

########################################################################


def process():

    print "%4s %s %6s %8s %-20s %20s %8s" % (
        "Sign",
        "Match",
        "Actual",
        "Expected",
        "(B, I, N, G, O)",
        "text",
        "equation"
    )

    equation_results = []
    equations_checksum = 0
    for index, sign_csum in enumerate(zip(SIGNS, CHECKSUMS)):

        sign, csum = sign_csum

        checksum, bingo, equation_result = compute_sign_values(
            sign,
            EQUATIONS[index]
        )

        equation_results.append(equation_result)
        equations_checksum += equation_result

        short = sign
        if len(short) >= 17:
            short = short[:17] + "..."

        print "%4d %5s %6d %8d %-20s %20s %8d" % (
            index + 1,
            (checksum == csum),
            checksum,
            csum,
            pformat(bingo),
            short,
            equation_result
        )

    print
    print "Equations checksum"
    print "%-5s %9s %9s" % ("BOOL", "Computed", "Expected")
    print "%-5s %9d %9d" % (
        (equations_checksum == EQUATIONS_CHECKSUM),
        equations_checksum,
        EQUATIONS_CHECKSUM
    )

    interpolate = dict(
        zip(
            ["S%d" % x for x in range(1, 14 + 1)],
            equation_results
        )
    )
    coordinates = u"N %(S1)s%(S2)s %(S3)s%(S4)s.%(S5)s%(S6)s%(S7)s " \
        u"W 0%(S8)s%(S9)s %(S10)s%(S11)s.%(S12)s%(S13)s%(S14)s" % interpolate

    print
    print coordinates

########################################################################

if __name__ == '__main__':

    import sys
    import os
    import traceback
    import optparse
    import time

########################################################################

    def main(args, options):

        print
        print 72 * '#'
        print

        filename = "bingo.txt"
        print
        print "Reading %s" % filename

        global SIGNS
        SIGNS = open(filename, "r").readlines()
        for index in range(len(SIGNS)):
            SIGNS[index] = SIGNS[index].strip()

        print "SIGNS:"
        pprint(SIGNS)
        print
        print 72 * '#'
        print

        process()

########################################################################

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version=__VERSION__
        )

        parser.add_option(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        (options, args) = parser.parse_args()

        if options.verbose:
            print time.asctime()

        exit_code = main(args, options)

        if exit_code is None:
            exit_code = 0

        if options.verbose:
            print time.asctime()
            print 'TOTAL TIME IN MINUTES:',
            print (time.time() - start_time) / 60.0

        sys.exit(exit_code)

    except KeyboardInterrupt, e:        # Ctrl-C
        raise e

    except SystemExit, e:               # sys.exit()
        raise e

    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

    # end of file
