#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Mon 01 Sep 2014 08:49:31 PM CDT
# Last Modified: Mon 01 Sep 2014 10:09:30 PM CDT

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

X_TRIBUTE_LOCATION = """N38 38.461 W90 33.857"""
X_LAT = 38 + 38.461 / 60.
X_LON = -(90 + 33.857 / 60.)
X_LATLON = (X_LAT, X_LON)

BAILEYS_LOCATION = "N38 38.500 W90 33.657"
B_LAT = 38 + 38.500 / 60.
B_LON = -(90 + 33.657 / 60.)
B_LATLON = (B_LAT, B_LON)

BOOKLIGHT_LOCATION = "N38 38.732 W90 33.856"
L_LAT = 38 + 38.732 / 60.
L_LON = -(90 + 33.856 / 60.)
L_LATLON = (L_LAT, L_LON)

BETA_LOCATION = "N38 38.537 W090 33.879"
C_LAT = 38 + 38.537 / 60.
C_LON = -(90 + 33.879 / 60.)

import simplekml
from geopy.distance import great_circle


def add_known_caches(kml):
    # add the nearby geocaches
    pnt = kml.newpoint(name="X Tribute", coords=[(X_LON, X_LAT)])
    pnt.style.iconstyle.color = simplekml.Color.red
    pnt = kml.newpoint(name="Baileys Cache", coords=[(B_LON, B_LAT)])
    pnt.style.iconstyle.color = simplekml.Color.red
    pnt = kml.newpoint(name="Booklight Cache", coords=[(L_LON, L_LAT)])
    pnt.style.iconstyle.color = simplekml.Color.red
    # add the dog park location
    pnt = kml.newpoint(name="BETA TEST", coords=[(C_LON, C_LAT)])
    pnt.style.iconstyle.color = simplekml.Color.green


def too_close(lat, lon):
    """Determine whether (lat, lon) is too close to nearby caches"""
    latlon = (lat, lon)

    d = great_circle(X_LATLON, latlon).miles
    if d < 0.1:
        return True

    d = great_circle(B_LATLON, latlon).miles
    if d < 0.1:
        return True

    d = great_circle(L_LATLON, latlon).miles
    if d < 0.1:
        return True

    return False


def ll_convert(s):
    sign, degrees, minutes = s[0], float(s[1:3]), float(s[4:])
    negative = False
    if sign in ['S', 'W']:
        negative = True
    angle = degrees + minutes / 60.
    if negative:
        angle = -angle
    return angle


def process():

    kml = simplekml.Kml()
    add_known_caches(kml)

    for hundredths in xrange(100):
        for lat_major in [4, 5, 6]:
            latitude = "N38 38.%d%02d" % (lat_major, hundredths)
            lat = ll_convert(latitude)
            for lon_major in [6, 7, 8, 9]:
                longitude = "W90 33.%d%02d" % (lon_major, hundredths)
                lon = ll_convert(longitude)
                if too_close(lat, lon):
                    continue
                name = "N%d_%d_%02d" % (lat_major, lon_major, hundredths)
                kml.newpoint(name=name, coords=[(lon, lat)])
    kml.save("TheDogAte.kml")

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

        #   if len(ARGS) < 1:
        #       PARSER.error ('missing argument')

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
