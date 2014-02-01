#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Sat 01 Feb 2014 12:57:36 PM CST
# Last Modified: Sat 01 Feb 2014 01:24:00 PM CST

"""
SYNOPSIS

    compute_closest_waypoints [-h] [-v,--verbose] [--version]

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

from find_trackpoint import find_trackpoint
from find_nearest_gc import find_nearest_gc
import sys

########################################################################

PICKLE = True

########################################################################


def compute_closest_waypoints(
    picture_datetimes,
    trackpoint_datetimes,
    geocache_locations,
    debug=False
):
    """
    Compute the closest waypoint for each of the pictures by correlating the
    filename/timestamp against the trackpoint timestamps and the
    geocache/waypoint locations
    """

    print >> sys.stderr, "compute_closest_waypoints"

    closest_waypoints = []
    for time, filename in picture_datetimes:

        # locate a nearby trackpoint
        tp = find_trackpoint(time, trackpoint_datetimes)

        if debug:
            print "compute_closest_waypoints: time: %s tp: %s" % (
                time,
                str(tp)
            )

        # find a nearby waypoint
        gc = find_nearest_gc(tp, geocache_locations, debug)

        closest_waypoints.append((time, filename, gc, tp))
        # print the result
        # print "time: %s\tfilename: %s\ttp: (%s, %s)" % (
        #     time,
        #     filename,
        #     gc,
        #     tp
        # )

    if PICKLE:
        from pickle import dump
        dump(closest_waypoints, open("closest_waypoints.dmp", "w"))

    return closest_waypoints

########################################################################

if __name__ == '__main__':

#   import sys
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

    def unpickle(filename):
        from pickle import Unpickler
        return Unpickler(open(filename)).load()

    def main():

        from pprint import pprint

        global options, args
        debug = options.debug

        picture_datetimes = unpickle("picture_datetimes.dmp")
        if debug:
            pprint(picture_datetimes)

        trackpoint_datetimes = unpickle("trackpoint_datetimes.dmp")
        if debug:
            pprint(trackpoint_datetimes)

        geocache_locations = unpickle("geocache_locations.dmp")
        if debug:
            pprint(geocache_locations)

        compute_closest_waypoints(
            picture_datetimes,
            trackpoint_datetimes,
            geocache_locations,
            debug
        )

########################################################################

    try:
        start_time = time.time()

        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version=__VERSION__
        )

        parser.add_option(
            '-d',
            '--debug',
            action='store_true',
            default=False,
            help='debug output'
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
