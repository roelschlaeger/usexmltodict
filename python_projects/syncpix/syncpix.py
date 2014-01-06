#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Fri 03 Jan 2014 03:26:18 PM CST
# Last Modified: Mon 06 Jan 2014 11:50:33 AM CST

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

from datetime import datetime
from find_nearest_gc import find_nearest_gc
from make_html import make_html
from pprint import pprint
from xml.etree import ElementTree as ET
import dateutil.parser
import os
import re

########################################################################

def maketag(gpxtag, gpx, new):
    return gpxtag.replace(gpx, new)

ROOTTAG = "{http://www.topografix.com/GPX/1/1}gpx"

DESCTAG   = maketag(ROOTTAG, "gpx", "desc")
NAMETAG   = maketag(ROOTTAG, "gpx", "name")
TIMETAG   = maketag(ROOTTAG, "gpx", "time")
TRKPTTAG  = maketag(ROOTTAG, "gpx", "trkpt")
TRKSEGTAG = maketag(ROOTTAG, "gpx", "trkseg")
TRKTAG    = maketag(ROOTTAG, "gpx", "trk")
WPTTAG    = maketag(ROOTTAG, "gpx", "wpt")

#######################################################################

def get_picture_data(dirname, timezone, debug=False):
    """Return a list of (datetime, filename) tuple objects"""

    print "Reading pictures from %s" % dirname

    filenames = os.listdir(dirname)

    picture_times = [ (x.split('.')[0], x) for x in filenames if x.find('.jpg') != -1 ]

    if debug:
        print "picture_times"
        pprint(picture_times, width=132)
        print

    picture_datetimes_nozone = [ (datetime.strptime(x[:10], "%m%d%y%H%M"), xf) for x, xf in picture_times ]
    picture_datetimes = [ (dateutil.parser.parse( str(x[0]) + timezone), x[1]) for x in picture_datetimes_nozone ]

    picture_datetimes.sort()

    if debug:
        print "picture_datetimes_nozone"
        pprint(picture_datetimes_nozone, width=132)
        print
        print "picture_datetimes"
        pprint(picture_datetimes, width=132)
        print

    return picture_datetimes

########################################################################

def get_trackpoint_datetimes(filename, debug=False):
    """Parse the 'filename' .gpx file for the longest trackpoint list,
    returning a list of (datetime, lon, lat) tuples in time order"""

    tree = ET.parse(filename)
    root = tree.getroot()
    tracks = root.findall(TRKTAG)
    if debug:
        print "tracks"
        pprint(tracks, width=132)
        print

    longest = (0, tracks[0].find(TRKSEGTAG).findall(TRKPTTAG))
    if debug:
        print "longest"
        pprint(longest, width=132)
        print

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
    if debug:
        print "trkpts"
        pprint(trkpts)
        print

    # build a list of (time, lon, lat) tuples, should already be in time order
    trackpoints = []

    for trkpt in trkpts:
        lat = float(trkpt.attrib["lat"] or 0.0)
        lon = float(trkpt.attrib["lon"] or 0.0)
        rawtime = trkpt.find(TIMETAG).text
        time = dateutil.parser.parse(rawtime)
#       print lat, lon, time
        trackpoints.append( (time, lon, lat) )

    if debug:
        print "trackpoints"
        pprint(trackpoints)
        print

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

        if re.match('^\d\d\d$', name):
            continue

        geocache_locations.append( (lon, lat, name, desc) )
        if debug:
            print (lon, lat, name, desc)

    gfile = open('geocache_locations.tmp', 'w')
    pprint(geocache_locations, gfile, width=132, indent=4) 
    gfile.close()

    return geocache_locations

########################################################################

def find_trackpoint(time, trackpoint_datetimes):
    """"Locates time in trackpoint_datetimes, returns (lat, lon) of
    corresponding location"""

    # time is datetime
    # trackpoint_datetimes is list of (datetime, lat, lon)

    for rtime, rlon, rlat in trackpoint_datetimes:
        if rtime > time:
            return (rlat, rlon)
    return trackpoint_datetimes[0][1:2]

########################################################################

def compute_closest_waypoints( picture_datetimes, trackpoint_datetimes, geocache_locations):

    print "compute_closest_waypoints"

    results = []
    for time, filename in picture_datetimes:

        # locate a nearby trackpoint
        tp = find_trackpoint(time, trackpoint_datetimes)

        # find a nearby waypoint
        gc = find_nearest_gc(tp, geocache_locations)

        results.append( (time, filename, gc, tp))
        # print the result
        print "time: %s\tfilename: %s\ttp: (%s, %s)" % (time, filename, gc, tp )

    if 1 or debug:
        resultfile = open("resultfile.txt", "w")
        pprint(results, resultfile, width=132)
        resultfile.close()

    return results

#######################################################################

def syncpix(route_name, pixdir, gpxfile, timezone):
    """Create an HTML file containing a table of pictures vs. waypoints"""

    # collect timestamps for pictures
    picture_datetimes = get_picture_data(pixdir, timezone, options.debug)

    # collect timestamps for trackpoints
    trackpoint_datetimes = get_trackpoint_datetimes(gpxfile, options.debug)

    # locate geocaches
    geocache_locations = get_geocache_locations(gpxfile, options.debug)

    # compute results
    results = compute_closest_waypoints(picture_datetimes, trackpoint_datetimes, geocache_locations)

    # create an html file
    make_html(pixdir, route_name, results)

#######################################################################

if __name__ == '__main__':

    import sys
    import os
    import traceback
    import optparse
    import time

    DATE = "20140104"
    PIXDIR = r"C:\Users\Robert Oelschlaeger\Google Drive\Caching Pictures\%s" % DATE
    ROUTE_NAME = "topo727 - Cape Girardeau MO"
    # GPXFILE = r"C:\Users\Robert Oelschlaeger\Dropbox\Geocaching\Explorist Results\explorist_results_%s.gpx" % DATE
    GPXFILE = r"%s\explorist_results_%s.gpx" % (PIXDIR, DATE)
    TIMEZONE = "CST"

    ########################################################################

    def main ():

        global options, args

        syncpix(ROUTE_NAME, PIXDIR, GPXFILE, TIMEZONE)

   ########################################################################

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
