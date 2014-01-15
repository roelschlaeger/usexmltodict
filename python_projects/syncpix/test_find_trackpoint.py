#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Mon 13 Jan 2014 03:21:52 PM CST
# Last Modified: Wed 15 Jan 2014 03:29:53 PM CST

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

from datetime import datetime
from pprint import pprint
from syncpix import find_trackpoint
import pickle
import pytz
import unittest

########################################################################

TIMEZONE = pytz.timezone("US/Central")

DATE = "20140111"
HOME = r"C:\Users\Robert Oelschlaeger"
PIXDIR = r"%s\Google Drive\Caching Pictures\%s" % (HOME, DATE)
GPXFILE = r"%s\explorist_results_%s.gpx" % (PIXDIR, DATE)

########################################################################


class tests(unittest.TestCase):

    # class variable
    trackpoint_datetimes = pickle.load(open("trackpoints.dmp"))
#   pprint(trackpoint_datetimes, open("trackpoints.txt", "w"))

#   def test_get_trackpoint_datetimes(self):
#       from syncpix import get_trackpoint_datetimes
#       filename = GPXFILE
#       trackpoints = get_trackpoint_datetimes(filename)
#       assert(
#           len(trackpoints) == 8048,
#           "Expected 8048, got %d" % len(trackpoints)
#       )

    def test_find_trackpoint(self):

#       self.one_test(datetime(2014, 01, 11, 13, 59, tzinfo=TIMEZONE))
#       self.one_test(datetime(2014, 01, 11, 14, 59, tzinfo=TIMEZONE))
#       self.one_test(datetime(2014, 01, 11, 15, 59, tzinfo=TIMEZONE))

        self.one_test(
            datetime(2014, 01, 11, 15,  7, tzinfo=TIMEZONE),
            (37.30487972, -89.55447310)
        )
        self.one_test(
            datetime(2014, 01, 11, 15,  8, tzinfo=TIMEZONE),
            (37.30503025, -89.55445558)
        )
        self.one_test(
            datetime(2014, 01, 11, 15,  9, tzinfo=TIMEZONE),
            (37.30528062, -89.55386046)
        )
        self.one_test(
            datetime(2014, 01, 11, 15, 10, tzinfo=TIMEZONE),
            (37.30528062, -89.55386046)
        )

    def one_test(self, time, check_values=None):
        print time
        result = find_trackpoint(time, self.trackpoint_datetimes)
        pprint(result)
        if not check_values is None:
            assert result == check_values, \
                "Expected %s, got %s" % (str(check_values), str(result))

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

        unittest.main()

########################################################################

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version=__VERSION__)
        parser.add_option(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )
        (options, args) = parser.parse_args()
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.verbose:
            print time.asctime()
        exit_code = main()
        if exit_code is None:
            exit_code = 0
        if options.verbose:
            print time.asctime()
        if options.verbose:
            print 'TOTAL TIME IN MINUTES:',
        if options.verbose:
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

# vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
