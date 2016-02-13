#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Fri 12 Feb 2016 04:37:06 PM CST
# Last Modified: Sat 13 Feb 2016 10:11:27 AM CST

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

from LatLon23 import LatLon, GeoVector
from simplekml import Kml

DOVE = (38.600483, -90.448933)  # location of the Dove sculpture at West County
FEET_PER_ROW = 275.13  # row multiplier to get feet
DEGREES_PER_CAP = 10.12  # cap multiplier to get degrees
FEET_TO_KM = 3280.84  # feet per kilometer


def projection(location, distance, bearing):
    """Make a projection
        from location = (latitude, longitude)
        by distance (in feet) and
        by bearing (in degrees)
        returning at LatLon object
    """
    km = distance / FEET_TO_KM
    latlon = LatLon(*location) + \
        GeoVector(initial_heading=bearing, distance=km)
    return latlon


def job():
    # open a new KML file
    kml = Kml()

    print " r  c    dist   bear     lat        lon"

    # row checksum is 8
    for rows in range(8, 100, 9):

        # compute the distance in feet
        distance = rows * FEET_PER_ROW


        # caps checksum is 10
        for caps in range(10, 100, 9):

            # compute the bearing in degrees
            bearing = caps * DEGREES_PER_CAP

            # check for too far
            if bearing >= 360.:
                break

            # make the projection
            proj = projection(DOVE, distance, bearing)

            # get the components
            lat = proj.lat
            lon = proj.lon
            print "%2d %2d %8.2f %6.2f %f %f" % (
                rows, caps, distance, bearing, lat, lon
            )

            # compute a name based on rows and caps
            name = "R%d_C%d" % (rows, caps)

            # add a new KML point
            kml.newpoint(name=name, coords=[(lon, lat)])

        print

    kml.save('cachemas2015_day10.kml')

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

#       global OPTIONS

#       # TODO: Do something more interesting here...
#       print 'Hello world!'

        job()

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
