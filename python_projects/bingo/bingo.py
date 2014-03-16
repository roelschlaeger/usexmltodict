#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Fri 14 Mar 2014 09:52:02 AM CDT
# Last Modified: Sun 16 Mar 2014 02:07:28 PM CDT

"""
SYNOPSIS

    bingo.py [-h] [-v,--verbose] [--version]

DESCRIPTION

    Compute checksums and coordinates for "Rest Stop BINGO" based on text
    strings in "bingo.txt".

    http://www.geocaching.com/
    geocache/
    GC4YPE2_rest-stop-bingo?guid=1b22b3c1-fc9f-4824-ac92-af4de6f9a395

USAGE EXAMPLES

    python bingo.py

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Robert Oelschlaeger <roelschlaeger@gmail.com>

LICENSE

    This script is in the public domain.

"""

__VERSION__ = "1.0.4"
"""Version string"""

########################################################################

from pprint import pformat, pprint
from collections import defaultdict

########################################################################

SIGNS = []
"""List of strings, one per sign"""

# these are the expected checksums from each of the signs
CHECKSUMS = [
    8,                                  # Sign 1
    118,                                # Sign 2
    5,                                  # Sign 3
    7,                                  # Sign 4
    87,                                 # Sign 5
    14,                                 # Sign 6
    3,                                  # Sign 7
    5,                                  # Sign 8
    2,                                  # Sign 9
    0,                                  # Sign 10
    39,                                 # Sign 11
    7,                                  # Sign 12
    4,                                  # Sign 13
    13,                                 # Sign 14
]
"""List of numbers, the checksums for the BINGO characters on each sign"""

BINGO_COLUMN_SUMS = [15, 75, 101, 30, 91]
"""column sums across all fourteen signs"""

# these are the equations to be applied for each sign
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
"""List of functions f(B, I, N, G, O) corresponding to each sign"""

# the expected checksum of all the equation results
EQUATIONS_CHECKSUM = 67
"""Checksum of all equation results"""

########################################################################


def compute_sign_values(sign, equation):
    """Count 'B', 'I', 'N', 'G', and 'O' characters in L{sign}, then compute
    L{equation} using the BINGO counts.

    @param sign: text string of the sign's message
    @type sign: string
    @param equation: a function of (B, I, N, G, O)
    @type equation: function
    @return: checksum, tuple, number
    @rtype: tuple
"""

    # convert to uppercase
    sign = sign.upper()

    # create a dictionary for the results
    counter_dictionary = defaultdict(lambda: 0)

    # count the letters
    for character in sign:
        counter_dictionary[character] += 1

    # collect the results for 'B', 'I', 'N', 'G' and 'O', computing the
    # checksum of the counts
    bingo_result_list = []
    checksum = 0
    for character in "BINGO":
        value = counter_dictionary[character]
        checksum += value
        bingo_result_list.append(value)

    # convert the result list to an immutable tuple
    result_tuple = tuple(bingo_result_list)

    # attempt to compute the equation result, watching out for division by zero
    try:
        equation_result = equation(*result_tuple)
    except ZeroDivisionError:
        equation_result = 99999999

    # return all of the results
    return checksum, result_tuple, equation_result

########################################################################


def print_column_checksums(bingo_column_sums):
    """Display the column sum differences nicely formatted"""

    print
    print "Column Checksums"
    print "================"
    print "Expected: ", pformat(BINGO_COLUMN_SUMS)
    print "Actual:   ", pformat(bingo_column_sums)
    print "          ", pformat(
        [
            BINGO_COLUMN_SUMS[i] == bingo_column_sums[i]
            for i in range(5)
        ]
    )

########################################################################


def print_equation_checksum(equations_checksum):
    """Display equation checksums nicely formatted"""

    print
    print "Equations checksum"
    print "=================="
    print "%-5s %9s %9s" % ("BOOL", "Computed", "Expected")
    print "%-5s %9d %9d" % (
        (equations_checksum == EQUATIONS_CHECKSUM),
        equations_checksum,
        EQUATIONS_CHECKSUM
    )

########################################################################


def process():
    """Compute and display BINGO results for all signs"""

    print "%4s %s %6s %8s %-20s %20s %8s" % (
        "Sign",
        "Match",
        "Actual",
        "Expected",
        "(B, I, N, G, O)",
        "text",
        "equation"
    )
    print "==== ===== ====== ======== ===============                      ==== ========"

    bingo_column_sums = [0, 0, 0, 0, 0]
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

        for index, column in enumerate(bingo):
            bingo_column_sums[index] += column

    print_column_checksums(bingo_column_sums)

    print_equation_checksum(equations_checksum)

    interpolate = dict(
        zip(
            ["S%d" % x for x in range(1, 14 + 1)],
            equation_results
        )
    )
    coordinates = u"N %(S1)s%(S2)s %(S3)s%(S4)s.%(S5)s%(S6)s%(S7)s " \
        u"W 0%(S8)s%(S9)s %(S10)s%(S11)s.%(S12)s%(S13)s%(S14)s" % interpolate

    print
    print "coordinates: %s" % coordinates

########################################################################

if __name__ == '__main__':

    import sys
    import os
    import traceback
    import optparse
    import time

########################################################################

    def main():
        """Required main program"""

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

        return 0

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
