#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Tue 04 Mar 2014 06:50:34 PM CST
# Last Modified: Wed 05 Mar 2014 04:11:53 PM CST

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

import pickle
from itertools import groupby
from collections import defaultdict
from pprint import pprint, pformat

########################################################################

WIDTH = 160

########################################################################


def load(f):
    db = pickle.load(open(f))
    return db


# ('2002-07-13', 'Missouri', 'Camden', 'GC22BB', 'Elephant Rocks!!! by Captain Ahab (2/3)')
def sortkeyfunc(db):
    "sort by state, county fields"
    return "%s_%s" % (db[1], db[2])

def keyfunc(db):
    "sort by state, county field"
    return "%s_%s" % (db[1], db[2])


def process(debug=False):

    db = load('roadwarrior.pkl')

    # sort by state & county
    sdb = sorted(db, key=sortkeyfunc)

    groups = defaultdict(list)
    unique_state_county = []

    # group by date
    for k, g in groupby(sdb, keyfunc):
        unique_state_county.append(k)
        groups[k].append(list(g))

    if debug:
        print 80 * '-'
        for k in unique_state_county:
            print k, pformat(groups[k], width=WIDTH)
            assert len(groups[k]) == 1, "Length error"
            print

    def county(r):
        result = "%s %s" % (r[1], r[2])
        return result

    counties_by_date = []

    if debug:
        print 80 * '='

    for state_county in unique_state_county:
        caches = groups[state_county][0]

        if debug:
            print state_county, len(caches), "\n", pformat(caches, width=WIDTH)
            print

        counties = []

        for k, g in groupby(caches, county):
            gl = list(g)
            counties.append((state_county, k, len(gl), (gl)))

        counties_by_date.append(counties)

    if debug:
        print 80 * '#'
        pprint(counties_by_date)

    for item in counties_by_date:
        state_county = item[0][0]
        formatted_string = "%-40s: %5d Caches" % (state_county, len(item[0]))
        print formatted_string

########################################################################

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

        debug = options.debug
        process(debug)

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

        parser.add_option(
            '-d',
            '--debug',
            action='store_true',
            default=False,
            help='debug output'
        )

        (options, args) = parser.parse_args()

        #   if len(args) < 1:
        #       parser.error ('missing argument')

        if options.verbose:
            print time.asctime()

        exit_code = main()

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
