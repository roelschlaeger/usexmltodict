#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Mon 06 Jul 2015 01:56:16 PM CDT
# Last Modified: Mon 06 Jul 2015 06:07:42 PM CDT

"""
SYNOPSIS

    outer_road [-h | --help] [-v | --version] [--verbose]

DESCRIPTION

    Generate graphical solutions to the Outer Road geocache (GC31919)

EXAMPLES

    outer_road

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

import simplekml
from geopy.distance import vincenty

CENTER = "N38 29.570 W91 59.810"


def convert(s):
    """Convert a latitude or longitude string to a float"""
    hemi, s = s[0].upper(), s[1:]
    sd, sm = map(float, s.split())
    print hemi, sd, sm
    sd += (sm / 60.000)
    if (hemi == 'W') or (hemi == 'S'):
        return -sd
    return sd


def dist(p1, p2):
    """Compute the Vincenty distance between p1 and p2"""
    # p1 = (latitude, longitude)
    # p2 = (latitude, longitude)
    return vincenty(p1, p2).miles


def dsum(n):
    """Compute the sum of the digits in the 7-digit string n"""
    return sum(map(int, list("%s" % n)))


def get_latitudes():
    """Compute latitudes within about a mile of CENTER that have a digit sum of
33"""

    lats = []
    for lat in range(3828000, 3830000):
        if dsum(lat) == 33:
            lats.append(lat)
    return lats


def get_longitudes():
    """Compute longitudes within about a mile of CENTER that have a digit sum
of 19"""

    lons = []
    for lon in range(9158000, 9160000):
        if dsum(lon) == 19:
            lons.append(lon)
    for lon in range(9200000, 9201000):
        if dsum(lon) == 19:
            lons.append(lon)
    return lons


def process():

    # locate the center point
    p1 = (convert(CENTER[:11]), convert(CENTER[11:]))

    # compute latitude and longitude grid points
    lats = get_latitudes()
    lons = get_longitudes()

    # set up for KML output
    kml = simplekml.Kml()

    # for each latitude string
    for slat in lats:

        # create a new KML folder
        folder = kml.newfolder(name="LAT_%s" % slat)

        # compute a latitude float value
        latd, latm = divmod(slat, 100000)
        latm /= 1000.
        lat = float(latd) + latm / 60.000

        # for each longitude string
        for slon in lons:

            # compute a longitude float value (assumed 'W', so negative)
            lond, lonm = divmod(slon, 100000)
            lonm /= 1000.
            lon = -(float(lond) + lonm / 60.000)

            # form endpoint tuple
            p2 = (lat, lon)

            # compute distance from centerpoint
            if dist(p1, p2) <= 1.0:

                # add the point to the latitude folder
                name = "%s_%s" % (slat, slon)
                folder.newpoint(
                    name=name,
                    coords=[(lon, lat)]
                )

    # output the file
    kml.save("outer_road.kml")

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
