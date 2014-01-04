#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Fri 03 Jan 2014 03:26:18 PM CST
# Last Modified: Fri 03 Jan 2014 10:41:58 PM CST

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

VERSION

    
"""

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

from pprint import pprint
from find_nearest_gc import find_nearest_gc

########################################################################

DATE = "20131217"
PIXDIR = r"C:\Users\Robert Oelschlaeger\Google Drive\Caching Pictures\%s" % DATE
GPXFILE = r"C:\Users\Robert Oelschlaeger\Dropbox\Geocaching\Explorist Results\explorist_results_%s.gpx" % DATE

########################################################################

from xml.etree import ElementTree as ET
from datetime import datetime

ROOTTAG = "{http://www.topografix.com/GPX/1/1}gpx"

def maketag(gpxtag, gpx, new):
    return gpxtag.replace(gpx, new)

DESCTAG   = maketag(ROOTTAG, "gpx", "desc")
NAMETAG   = maketag(ROOTTAG, "gpx", "name")
TIMETAG   = maketag(ROOTTAG, "gpx", "time")
TRKPTTAG  = maketag(ROOTTAG, "gpx", "trkpt")
TRKSEGTAG = maketag(ROOTTAG, "gpx", "trkseg")
TRKTAG    = maketag(ROOTTAG, "gpx", "trk")
WPTTAG    = maketag(ROOTTAG, "gpx", "wpt")

########################################################################

#   def closest_wpt(lat, lon, waypoints):
#       from geodesic import Geodesic
#   
#       for waypoint in waypoints:
#           wlat = None
#           wlon = None
#           dist = Geodesic.WGS84.Inverse(lat, lon, wlat, wlon)['s12']

########################################################################

def get_picture_data(dirname, debug=False):
    """Return a list of (datetime.datetime, filename) tuple objects"""

    filenames = os.listdir(dirname)

    picture_times = [ x.split('.')[0] for x in filenames ]

    if debug:
        pprint(picture_times)

    picture_datetimes = [ (datetime.strptime(x, "%m%d%y%H%M"), x) for x in picture_times ]

    picture_datetimes.sort()

    if debug:
        pprint(picture_datetimes)

    return picture_datetimes

########################################################################

def get_trackpoint_datetimes(filename, debug=False):
    """Parse the 'filename' .gpx file for the longest trackpoint list,
    returning a list of (datetime, lon, lat) tuples in time order"""

    tree = ET.parse(filename)
    root = tree.getroot()
    tracks = root.findall(TRKTAG)
    if debug:
        pprint(tracks)

    longest = (0, tracks[0].find(TRKSEGTAG).find(TRKPTTAG))

    if len(tracks) > 1:

        for track in tracks:

            name = track[0].text
            print track, name,

            tracksegment = track.find(TRKSEGTAG)
            trkpts = tracksegment.findall(TRKPTTAG)
            print len(trkpts)

            if len(trkpts) > longest[0]:
                longest = (len(trkpts), trkpts)

            print '########################################################################'

    # for now, just take the longest list
    trkpts = longest[1]

    # build a list of (time, lon, lat) tuples, should already be in time order
    trackpoints = []

    for trkpt in trkpts:
        lat = float(trkpt.attrib["lat"])
        lon = float(trkpt.attrib["lon"])
        rawtime = trkpt.find(TIMETAG).text
        time = datetime.strptime(rawtime, "%Y-%m-%dT%H:%M:%SZ")
#       print lat, lon, time
        trackpoints.append( (time, lon, lat) )

    if debug:
        pprint(trackpoints)

    return trackpoints
    
########################################################################

def get_geocache_locations(filename, debug=False):

    tree = ET.parse(filename)
    root = tree.getroot()
    waypoints = root.findall(WPTTAG)

    geocache_locations = []
    for wpt in waypoints:
        lat = float(wpt.attrib["lat"])
        lon = float(wpt.attrib["lon"])
        name = wpt.find(NAMETAG).text
        # optional element
        desc = wpt.find(DESCTAG)
        if desc is not None:
            desc = desc.text

        geocache_locations.append( (lon, lat, name, desc) )
        if debug:
            print (lon, lat, name, desc)

    return geocache_locations

########################################################################

def find_trackpoint(time, trackpoint_datetimes):
    """"Locates time in trackpoint_datetimes, returns (lat, lon) of
    corresponding location"""

    print "find_trackpoint"

    # time is datetime.datetime
    # trackpoint_datetimes is list of (datetime, lat, lon)

    for rtime, rlon, rlat in trackpoint_datetimes:
        if rtime > time:
            return (rlat, rlon)
    return trackpoint_datetimes[0][1:2]

########################################################################

def compute_closest_waypoints( picture_datetimes, trackpoint_datetimes, geocache_locations):

    print "compute_closest_waypoints"

    for time, filename in picture_datetimes:
        print "time: %s filename: %s" % (time, filename)
        tp = find_trackpoint(time, trackpoint_datetimes)
        print "tp: (%s, %s)" % tp
        gc = find_nearest_gc(tp, geocache_locations)
        break

########################################################################

def main ():

    global options, args

    picture_datetimes = get_picture_data(PIXDIR, options.debug)
    trackpoint_datetimes = get_trackpoint_datetimes(GPXFILE, options.debug)
    geocache_locations = get_geocache_locations(GPXFILE, options.debug)
    compute_closest_waypoints( picture_datetimes, trackpoint_datetimes, geocache_locations)

########################################################################

if __name__ == '__main__':

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
                formatter=optparse.TitledHelpFormatter(),
                usage=globals()['__doc__'],
                version='$Id: py.tpl 332 2008-10-21 22:24:52Z root $')
        parser.add_option ('-d', '--debug', action='store_true',
                default=False, help='debug output')
        parser.add_option ('-v', '--verbose', action='store_true',
                default=False, help='verbose output')
        (options, args) = parser.parse_args()
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.verbose: print time.asctime()
        exit_code = main()
        if exit_code is None:
            exit_code = 0
        if options.verbose: print time.asctime()
        if options.verbose: print 'TOTAL TIME IN MINUTES:',
        if options.verbose: print (time.time() - start_time) / 60.0
        sys.exit(exit_code)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

# vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
