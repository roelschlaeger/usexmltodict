#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Tue 04 Mar 2014 06:50:34 PM CST
# Last Modified: Thu 06 Mar 2014 03:26:48 PM CST

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


def date_county_keyfunc(db):
    "sort by date, state, county fields"
    return (db[0], db[1], db[2])


def process():

    db = load('roadwarrior.pkl')

#   print db[:3]

    # sort by date
    sort_database = sorted(db, key=date_county_keyfunc)

    date_groups = defaultdict(list)
    unique_dates = []

    def date_keyfunc(db):
        return db[0]

    # group by date
    for k, g in groupby(sort_database, date_keyfunc):
        unique_dates.append(k)
        date_groups[k].append(list(g))

    print 80 * '-'
    for date in unique_dates:
        print date, pformat(date_groups[date], width=WIDTH)
        assert len(date_groups[date]) == 1, "Length error"
        print

    def state_county_keyfunc(r):
#       r = r[0]
        result = "%s %s" % (r[1], r[2])
        return result

    counties = defaultdict(list)

    print 80 * '='
    for date in unique_dates:

        county_group = date_groups[date][0]
        print "Date: %s len(county_group): %d" % (date, len(county_group))

        print date

        # now group them by county
        for k, g in groupby(county_group, state_county_keyfunc):
            gl = list(g)
            counties[date].append((k, len(gl)))

    print 80 * '#'
    pprint(counties, width=WIDTH)

    for date, county_list in counties.items():

        clist = [x[0] for x in county_list]
        formatted_string = "%s: %d Counties (%s)" % (
            date,
            len(county_list),
            ", ".join(clist)
        )
        print formatted_string
#       ts = item
#       for ts in item:
#       print "    %-25s %2s" % (ts[1], ts[2])
#       print

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
