#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 25 Jun 2015 04:59:23 PM CDT
# Last Modified: Sun 28 Jun 2015 09:50:12 AM CDT

"""
SYNOPSIS

    TODO omega [-h | --help] [-v | --version] [--verbose]

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

import simplekml
from simplekml import Kml
from polycircles import polycircles
from xml.etree import ElementTree as ET

########################################################################


def convert(s):
    """Convert a latitude or longitude hdd mm.mmm string to a signed floating
point value"""

    d, m = s.split()
    h, d = d[0], d[1:]
    negative = (h == 'W') or (h == 'S')
    result = int(d) + (float(m) / 60.)
    if negative:
        result = -result
    return result

########################################################################

RADIUS = 160.93   # 512.8 feet, in meters


def process(options):
    kml = Kml()

    lat_pattern = "N39 45.%s66"
    lon_pattern = "W89 45.8%s%s"

    f0 = kml.newfolder(name="Solution Locations")

    for C in range(10):
        for I in range(10):
            J = 5
            dmlat = lat_pattern % C
            dmlon = lon_pattern % (I, J)
            lat = convert(dmlat)
            lon = convert(dmlon)
            name = "P_C%s_I%s_J%s" % (C, I, J)
            f0.newpoint(name=name, coords=[(lon, lat)])

    if True or options.circles:

        f1 = kml.newfolder(name="GPX Point Centers")
        f2 = kml.newfolder(name="0.1 Mile Circles")

        points = getpoints(options.circles)

        for point in points:

            lat, lon, name, desc = point
            description = "%s: %s" % (name, desc)
            # create the center point

            f1.newpoint(
                name=description,
                coords=[(lon, lat)]
            )

            # create the outline
            polycircle = polycircles.Polycircle(
                latitude=lat,
                longitude=lon,
                radius=RADIUS,
                number_of_vertices=72
            )

            pol = f2.newpolygon(
                name=description,
                outerboundaryis=polycircle.to_kml(),
            )

            pol.description = description

            pol.style.polystyle.color = simplekml.Color.red
            pol.style.polystyle.outline = 1
            pol.style.polystyle.fill = 1

    kml.save("omega.kml")

########################################################################


def print_meta(meta):
    return

    seen = False
    for item in list(meta):
        if item.text is not None:
            text = item.text.strip()
            if text:
                print "%s: %s" % (item.tag, item.text)
                seen = True
    if seen:
        print

########################################################################


def getpoints(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    tag = root.tag
    wpt_tag = tag.replace('gpx', 'wpt')
    metadata_tag = tag.replace('gpx', 'metadata')
    name_tag = tag.replace('gpx', 'name')
    desc_tag = tag.replace('gpx', 'desc')

    print_meta(root.find(metadata_tag))

    points = []
    for wpt in root.findall(wpt_tag):
        lat = float(wpt.get('lat'))
        lon = float(wpt.get('lon'))
        name = wpt.find(name_tag).text
        desc = wpt.find(desc_tag).text
        latlon = (lat, lon, name, desc)
#       print latlon
        points.append(latlon)
    return points

########################################################################

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

    def main(options):

        process(options)

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

        PARSER.add_argument(
            '-c',
            '--circles',
            action='store',
            type=str,
            default="Five Miles.gpx",
            help='display 0.1 mile circles'
        )

        OPTIONS = PARSER.parse_args()

        if OPTIONS.verbose:
            print time.asctime()

        EXIT_CODE = main(OPTIONS)

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
