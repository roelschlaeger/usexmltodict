#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Fri 03 Jan 2014 03:26:18 PM CST
# Last Modified: Fri 03 Jan 2014 05:21:11 PM CST

"""
SYNOPSIS

    TODO syncpix [-h] [-v,--verbose] [--version]

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

NAMETAG = maketag(ROOTTAG, "gpx", "name")
TIMETAG = maketag(ROOTTAG, "gpx", "time")
TRKPTTAG = maketag(ROOTTAG, "gpx", "trkpt")
TRKSEGTAG = maketag(ROOTTAG, "gpx", "trkseg")
TRKTAG = maketag(ROOTTAG, "gpx", "trk")

def main ():

    global options, args

    filenames = os.listdir(PIXDIR)
    picture_times = [ x.split('.')[0] for x in filenames ]
    picture_datetimes = [ datetime.strptime("20%s" % x, "%m%d%H%M%S") for x in picture_times ]
    pprint(picture_datetimes)
    sys.exit(1)

    tree = ET.parse(GPXFILE)
    tree.write("this.gpx")

    root = tree.getroot()

    tracks = root.findall(TRKTAG)
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

#   pprint( longest )

    # for now, just take the longest list
    trkpts = longest[1]

    # build a list of (time, lon, lat) tuples
    trackpoints = []
    for trkpt in trkpts:
        lat = trkpt.attrib["lat"]
        lon = trkpt.attrib["lon"]
        rawtime = trkpt.find(TIMETAG).text
        time = datetime.strptime(rawtime, "%Y-%m-%dT%H:%M:%SZ")
        print lat, lon, time
        trackpoints.append( (time, lon, lat) )

    pprint(trackpoints)
    
if __name__ == '__main__':

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
                formatter=optparse.TitledHelpFormatter(),
                usage=globals()['__doc__'],
                version='$Id: py.tpl 332 2008-10-21 22:24:52Z root $')
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
