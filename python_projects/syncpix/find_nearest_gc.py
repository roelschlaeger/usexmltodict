#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Fri 03 Jan 2014 10:02:22 PM CST
# Last Modified: Fri 03 Jan 2014 10:44:55 PM CST

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

    TODO: Name <name@example.org>

LICENSE

    This script is in the public domain.

VERSION

    
"""

from geographiclib.geodesic import Geodesic

########################################################################

def distance(lat1, lon1, lat2, lon2):

    return Geodesic.WGS84.Inverse(lat1, lon1, lat2, lon2)['s12']

########################################################################

def find_nearest_gc(tp, geocache_locations):
    """
    tp is (lat, lon)
    geocache_locations is a list of (lon, lat, name, desc) tuples
    """

#   print "find_nearest_gc"

#   pprint(tp)
    lat, lon = tp

    min_d = None
    for glon, glat, gname, gdesc in geocache_locations:
        d = distance(lat, lon, glat, glon)
        if (min_d is None) or (d < min_d[0]):
            min_d = (d, gname, gdesc)

    return min_d

########################################################################

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

from test_geocache_locations import geocache_locations
from pprint import pprint
from random import choice

def main ():

    global options, args

    extent = 0.001

    for _ in range(20):
        gl = choice(geocache_locations)
        tp = (float(gl[1]) + extent, float(gl[0]) + extent)
        name = gl[2]

#       tp = (38.580, -90.4)
        print "\n", name, str(tp)

        result = find_nearest_gc(tp,  geocache_locations)

        pprint(result)

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
