#!/usr/bin/env python3
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8

# Created:       Fri 03 Jan 2014 03:26:18 PM CST
# Last Modified: Fri 15 Sep 2017 08:04:48 AM CDT

#######################################################################

"""
SYNOPSIS

    syncpix
        [--verbose]
        [-d --debug]
        [-h --help]
        [-v --version]
        [[-t --date] DDDDDDDD]

DESCRIPTION

    Synchronize pictures in PIXDIR with caches along a tracklist in GPXFILE

EXAMPLES

    TODO: Show some examples of how to use this script.

AUTHOR

    Robert L. Oelschlaeger <roelsc2009@gmail.com>

LICENSE

    This script is in the public domain.

"""

########################################################################

from datetime import datetime
from mh import make_html
from pprint import pprint
from xml.etree import ElementTree as ET
import dateutil.parser
import os
import pickle
import re
import sys
from compute_closest_waypoints import compute_closest_waypoints

#######################################################################

__VERSION__ = "0.2.2"

global PICKLE
PICKLE = False

ROOTTAG = "{http://www.topografix.com/GPX/1/1}gpx"

########################################################################


def make_tag_from_root(new):
    """Create a tag for 'new' based on 'gpx'"""
    return ROOTTAG.replace("gpx", new)

DESCTAG = make_tag_from_root("desc")
NAMETAG = make_tag_from_root("name")
TIMETAG = make_tag_from_root("time")
TRKPTTAG = make_tag_from_root("trkpt")
TRKSEGTAG = make_tag_from_root("trkseg")
TRKTAG = make_tag_from_root("trk")
WPTTAG = make_tag_from_root("wpt")

GEOCACHE_LOCATIONS_FILENAME = "geocache_locations.tmp"

#######################################################################

####################################################################
# the old way of getting picture date and times from picture names #
####################################################################

#    def get_picture_datetimes(dirname, timezone, debug=False):
#        """Return a list of (datetime, filename) tuple objects"""
#
#        print >> sys.stderr, "Reading pictures from %s" % dirname
#
#        filenames = os.listdir(dirname)
#
#        picture_times = [
#            (x.split('.')[0], x)
#            for x in filenames if x.find('.jpg') != -1
#        ]
#
#        if debug:
#            print "picture_times"
#            pprint(picture_times, width=132)
#            print
#
#        # get timestamp without time zone
#        picture_datetimes_nozone = [
#            (datetime.strptime(x[:10], "%m%d%y%H%M"), xf)
#            for x, xf in picture_times
#        ]
#
#        # append timezone
#        picture_datetimes = [
#            (dateutil.parser.parse(str(x[0]) + timezone), x[1])
#            for x in picture_datetimes_nozone
#        ]
#
#        # sort into time order
#        picture_datetimes.sort()
#
#        if debug:
#    #       print "picture_datetimes_nozone"
#    #       pprint(picture_datetimes_nozone, width=132)
#    #       print
#
#            print "picture_datetimes"
#            pprint(picture_datetimes, width=132)
#            print
#
#        if PICKLE:
#            pickle.dump(picture_datetimes, open("picture_datetimes.dmp", "w"))
#
#        return picture_datetimes

####################################################################
# the new way of getting picture date and times from picture names #
####################################################################


def get_picture_datetimes(dirname, timezone, debug=False):
    """Return a list of (datetime, filename) tuple objects
    based on filenames like

        IMG_20150610_073626_868.jpg

    instead of

        0610150736.jpg
    """

    import sys
    print("Reading pictures from %s" % dirname, file=sys.stderr)

    import os
    filenames = os.listdir(dirname)

    pprint(filenames)

    def mdyHM(x):
        """
IMG_20150610_073626_868.jpg
01234567890123456789012
"""
        # isolate the month, day, year, Hour and Minute fields
        m = x[8:10]
        d = x[10:12]
        y = x[6:8]
        H = x[13:15]
        M = x[15:17]

        # return the data as a date string
        return "%s%s%s%s%s" % (m, d, y, H, M)

    # collect (datestring, filename) tuples
    picture_times = [
        (mdyHM(x), x)
        for x in filenames if x.find('.jpg') != -1
    ]

    if debug:
        print("picture_times")
        pprint(picture_times, width=132)
        print()

    # get timestamp without time zone
    picture_datetimes_nozone = [
        (datetime.strptime(x[:10], "%m%d%y%H%M"), xf)
        for x, xf in picture_times
    ]

    # append timezone
    picture_datetimes = [
        (dateutil.parser.parse(str(x[0]) + timezone), x[1])
        for x in picture_datetimes_nozone
    ]

    # sort into time order
    picture_datetimes.sort()

    if debug:
        print("picture_datetimes")
        pprint(picture_datetimes, width=132)
        print()

    if PICKLE:
        pickle.dump(picture_datetimes, open("picture_datetimes.dmp", "w"))

    return picture_datetimes

########################################################################


def get_trkpts(filename, debug):
    """Get the trkpts from 'filename'"""

    print("Reading trkpts from %s" % filename, file=sys.stderr)

    tree = ET.parse(filename)
    root = tree.getroot()
    trkpts = []

    # look through all tracks
    for track in root.findall(TRKTAG):
        for index, track_segment in enumerate(track.findall(TRKSEGTAG)):
            trkpts.extend(track_segment.findall(TRKPTTAG))

    # save all trkpts
    if PICKLE:
        pickle.dump(trkpts, open("trkpts.dmp", "w"))

    return trkpts

########################################################################


def get_trackpoint_datetimes(filename, debug=False):
    """
    Parse the 'filename' .gpx file for the longest trackpoint list, returning a
    list of (datetime, lon, lat) tuples in time order
    """

    print("Reading track times from %s" % filename, file=sys.stderr)

    trkpts = get_trkpts(filename, debug)

    # build a list of (time, lon, lat) tuples, should already be in time order
    trackpoints = []

    for trkpt in trkpts:

        lat = float(trkpt.attrib["lat"] or 0.0)
        lon = float(trkpt.attrib["lon"] or 0.0)
        rawtime = trkpt.find(TIMETAG).text
        time = dateutil.parser.parse(rawtime)
        trackpoints.append((time, lon, lat))

    # ensure that the points are in time-sorted order
    trackpoints.sort()

    if PICKLE:
        pickle.dump(trackpoints, open("trackpoint_datetimes.dmp", "w"))

    return trackpoints

########################################################################


def optional(desc, otherwise="None"):
    if desc is None:
        desc = otherwise
    else:
        desc = desc.text
    return desc

########################################################################


def get_geocache_locations(filename, debug=False):
    """
    Create a list of geocache locations from the 'filename' .gpx file
    """

    print("Getting geocache locations from %s" % filename, file=sys.stderr)

    tree = ET.parse(filename)
    root = tree.getroot()
    waypoints = root.findall(WPTTAG)

    geocache_locations = []

    for wpt in waypoints:

        lat = float(wpt.attrib["lat"])
        lon = float(wpt.attrib["lon"])
        name = wpt.find(NAMETAG).text
        print(name)

        # optional element
        desc = optional(wpt.find(DESCTAG), "None")

        # skip \d\d\d waypoints generated by Garmin
        if re.match('^\d\d\d$', name):
            print("skipping: %s" % name)
            continue

        geocache_locations.append((lon, lat, name, desc))
        if debug:
            print((lon, lat, name, desc))

    if PICKLE:
        pickle.dump(geocache_locations, open("geocache_locations.dmp", "w"))

    return geocache_locations

#######################################################################


def syncpix(route_name, pixdir, gpxfile, timezone, debug=False):
    """Create an HTML file containing a table of pictures vs. waypoints"""

    if debug:
        print((
            'syncpix('
            'route_name="%s", '
            'pixdir="%s", '
            'gpxfile="%s", '
            'timezone="%s", '
            'debug="%s")' % (route_name, pixdir, gpxfile, timezone, debug)
        ))

    # collect timestamps for pictures
#   from bobo import new_get_picture_datetimes as get_picture_datetimes
    picture_datetimes = get_picture_datetimes(pixdir, timezone, debug)

    # collect timestamps for trackpoints
    trackpoint_datetimes = get_trackpoint_datetimes(gpxfile, debug)

    # locate geocaches
    geocache_locations = get_geocache_locations(gpxfile, debug)

    # compute closest_waypoints
    closest_waypoints = compute_closest_waypoints(
        picture_datetimes,
        trackpoint_datetimes,
        geocache_locations
    )

    # create an html file
    make_html(pixdir, route_name, closest_waypoints)

#######################################################################

if __name__ == '__main__':

    import argparse
    import textwrap
    import time
    import traceback

    DATE = "20170914"
    ROUTE_NAME = "topo913e - Sedalia MO"

    HOME = r"C:\Users\Robert Oelschlaeger"
    TIMEZONE = "CDT"

    ########################################################################

    def main(route_name, pixdir, gpxfile, timezone, debug):
        if debug:
            print("""
main(
    route="%s",
    pixdir="%s",
    gpxfile="%s",
    timezone="%s",
    debug=%s
)""" % (route_name, pixdir, gpxfile, timezone, debug))
        else:
            syncpix(route_name, pixdir, gpxfile, timezone, debug)

    ########################################################################

    try:

        start_time = time.time()

        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=textwrap.dedent(globals()['__doc__']),
#           version="Version: %s" % __VERSION__
        )

        parser.add_argument(
            '--debug',
            '-d',
            action='store_true',
            default=False,
            help='debug output'
        )

        parser.add_argument(
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        parser.add_argument(
            '--date',
            '-t',
            action='store',
            default=DATE,
            help='set date (default: %(default)s)'
        )

        parser.add_argument(
            '--pickle',
            '-p',
            action='store_true',
            default=False,
            help='set PICKLE flag'
        )

        parser.add_argument(
            '--route',
            '-r',
            action='store',
            default=ROUTE_NAME,
            help='set route (default: %(default)s)'
        )

        # parse command line options
        options = parser.parse_args()
        pprint(options)

        date_option = options.date
        route_name = options.route
        PICKLE = options.pickle

        pixdir = r"%s\Google Drive\Caching Pictures\%s" % (HOME, date_option)
        print("pixdir: %s" % pixdir)

        gpxfile = r"%s\explorist_results_%s.gpx" % (pixdir, date_option)
        print("gpxfile: %s" % pixdir)

        if options.verbose:
            print(time.asctime())

        exit_code = main(route_name, pixdir, gpxfile, TIMEZONE, options.debug)

        if exit_code is None:
            exit_code = 0

        if options.verbose:
            print(time.asctime())
            print('TOTAL TIME IN MINUTES:',)
            print((time.time() - start_time) / 60.0)

        sys.exit(exit_code)

    except KeyboardInterrupt as e:      # Ctrl-C
        raise e

    except SystemExit as e:             # sys.exit()
        raise e

    except Exception as e:
        print("Exception", e)
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)

# vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
