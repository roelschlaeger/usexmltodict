#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 23 Jul 2015 01:50:56 PM CDT
# Last Modified: Thu 23 Jul 2015 06:11:59 PM CDT

"""
SYNOPSIS

    TODO helloworld [-h | --help] [-v | --version] [--verbose]

DESCRIPTION

    This script is used to solve for locations that might be the hiding place
    for AYHE? #11 (GC5YT4C), based on the following translation:

        To retrieve the coordinates for the cache, you need to collect
        information on the posted coordinates and use this information to do a
        projection.

        To find the bearing of the projection, you have a table that list find
        four people who, Germany (together with three other persons) immigrated
        from Melle.  Record for each of the people who came from Melle the
        difference between their year of death and date of birth. Add up the
        four numbers, and add ten. This is the camp for projection in degree.
        The checksum for the camp's eleven.

        To find the distance for projection, you have to find two figures. The
        first number is the last two digits of the year associated with a
        person from Schlüesselberg, Germany. The second number is the sum of
        the last two digits in the book binding. Multiply these two numbers.
        This is the distance for the projection in meters. The checksum for the
        distance is fifteen.

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

VERSION

"""

__VERSION__ = "0.0.1"

########################################################################

from pprint import pprint
from pyproj import Geod
from simplekml import Kml

G = Geod(ellps="WGS84")

DMAX = 1609  # meters in a mile
# CENTER = (N 38° 42.524' W 090° 52.901')
CENTER = (38 + 42.524 / 60., -(90 + 52.901 / 60.))


def compute_distances():
    distances = []
    for d1 in range(1, 100):
        for d2 in range(1, 18 + 1):
            distance = d1 * d2
            if distance > DMAX:
                break
            if not distance in distances:
                distances.append(distance)
    return distances


def checksum(d):
    s = "%03d" % d
    return sum(map(int, s))


def compute_bearings():
    bearings = []
    for bearing in range(10, 360):
        if checksum(bearing) != 11:
            continue
        bearings.append(bearing)
    return bearings


def compute_locations(distances, bearings):
    """Returns (distance, bearing...)"""
    lats = [CENTER[0]]
    lons = [CENTER[1]]
    locations = []
    for distance in distances:
        for bearing in bearings:
            locations.append(
                (
                    distance,
                    bearing,
                    G.fwd(lons, lats, bearing, distance)
                )
            )
    return locations


def compute_points(locations):
    """Returns list of (distance, bearing, lat, lon)"""
    points = []
    for distance, bearing, triple in locations:
        lon_list, lat_list, reverse_az = triple
        lat = lat_list[0]
        lon = lon_list[0]
        points.append((distance, bearing, lat, lon))
    return points


def process():

    distances = sorted(compute_distances())

    # thin out the result by taking every 50th distance
    THIN = 50
    distances = distances[::THIN]
    pprint(distances)

    bearings = compute_bearings()

    locations = compute_locations(distances, bearings)

    points = compute_points(locations)

    kml = Kml()

    for distance, bearing, lat, lon in points:
        name = "d_%s_b_%s" % (distance, bearing)
        kml.newpoint(
            name=name,
            coords=[(lon, lat)]
        )

    kml.save("ayhe11.kml")


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
