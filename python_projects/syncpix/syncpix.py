#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8

# Created:       Fri 03 Jan 2014 03:26:18 PM CST
# Last Modified: Thu 18 Sep 2014 05:04:14 PM CDT

"""
SYNOPSIS

    syncpix [-h] [-v,--verbose] [--version] [-d, --debug]

DESCRIPTION

    Synchronize pictures in PIXDIR with caches along a tracklist in GPXFILE

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Name <name@example.org>

LICENSE

    This script is in the public domain.

"""

__VERSION__ = "0.1.0"

# from pexpect import run, spawn

# Uncomment the following section if you want readline history support.
#import readline, atexit
#histfile = os.path.join(os.environ['HOME'], '.TODO_history')
#try:
#    readline.read_history_file(histfile)
#except IOError:
#    pass
#atexit.register(readline.write_history_file, histfile)

#######################################################################

# from make_html import make_html
# from find_nearest_gc import find_nearest_gc

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

########################################################################

PICKLE = True

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


def get_picture_datetimes(dirname, timezone, debug=False):
    """Return a list of (datetime, filename) tuple objects"""

    print >> sys.stderr, "Reading pictures from %s" % dirname

    filenames = os.listdir(dirname)

    picture_times = [
        (x.split('.')[0], x)
        for x in filenames if x.find('.jpg') != -1
    ]

    if debug:
        print "picture_times"
        pprint(picture_times, width=132)
        print

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
#       print "picture_datetimes_nozone"
#       pprint(picture_datetimes_nozone, width=132)
#       print

        print "picture_datetimes"
        pprint(picture_datetimes, width=132)
        print

    if PICKLE:
        pickle.dump(picture_datetimes, open("picture_datetimes.dmp", "w"))

    return picture_datetimes

########################################################################


def get_trkpts(filename, debug):
    """Get the trkpts from 'filename'"""

    print >> sys.stderr, "Reading trkpts from %s" % filename

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

    print >> sys.stderr, "Reading track times from %s" % filename

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

    print >> sys.stderr, "Getting geocache locations from %s" % filename

    tree = ET.parse(filename)
    root = tree.getroot()
    waypoints = root.findall(WPTTAG)

    geocache_locations = []

    for wpt in waypoints:

        lat = float(wpt.attrib["lat"])
        lon = float(wpt.attrib["lon"])
        name = wpt.find(NAMETAG).text
        print name

        # optional element
        desc = optional(wpt.find(DESCTAG), "None")

       # skip \d\d\d waypoints generated by Garmin
        if re.match('^\d\d\d$', name):
            print "skipping: %s" % name
            continue

        geocache_locations.append((lon, lat, name, desc))
        if debug:
            print (lon, lat, name, desc)

    # write the geocache locations file
#   gfile = open(GEOCACHE_LOCATIONS_FILENAME, 'w')
#   pprint(geocache_locations, gfile, width=132, indent=4)
#   print "geocache locations results are in %s" % GEOCACHE_LOCATIONS_FILENAME
#   gfile.close()

    if PICKLE:
        pickle.dump(geocache_locations, open("geocache_locations.dmp", "w"))

    return geocache_locations

#######################################################################


def syncpix(route_name, pixdir, gpxfile, timezone, debug=False):
    """Create an HTML file containing a table of pictures vs. waypoints"""

    if debug:
        print(
            'syncpix('
            'route_name="%s", '
            'pixdir="%s", '
            'gpxfile="%s", '
            'timezone="%s", '
            'debug="%s")' % (route_name, pixdir, gpxfile, timezone, debug)
        )

    # collect timestamps for pictures
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

    import optparse
    import time
    import traceback
#   import os

    DATE = "20140917"
    ROUTE_NAME = "Florissant MO"

    HOME = r"C:\Users\Robert Oelschlaeger"
    PIXDIR = r"%s\Google Drive\Caching Pictures\%s" % (HOME, DATE)
    GPXFILE = r"%s\explorist_results_%s.gpx" % (PIXDIR, DATE)
    TIMEZONE = "CST"

    ########################################################################

    def main():

        global options, args

        syncpix(ROUTE_NAME, PIXDIR, GPXFILE, TIMEZONE, options.debug)

   ########################################################################

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version="Version: %s" % __VERSION__
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
