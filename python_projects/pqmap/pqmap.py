#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Wed 01 Jan 2014 03:01:01 PM CST
# Last Modified: Thu 02 Jan 2014 10:18:09 AM CST

"""
SYNOPSIS

    pqmap [-h] [-v,--verbose] [--version]

DESCRIPTION

    This function creates a KML file of the 'bounds' values found in all of the
    non-'wpts' files inside of .zip files in BASEDIR.
    
    This docstring will be printed by the script if there is an error or if the
    user requests help (-h or --help).

EXAMPLES

    python pqmap.py -v

        Thu Jan 02 09:59:07 2014
        12614439_B-2 Spirit -- Knob Noster MO.gpx                   	(38.096633, 39.376367, -94.342267, -92.779117)
        45606_Barnesville MO.gpx                                    	(38.939, 40.845517, -93.740133, -91.329033)
        46563_Bogota IL.gpx                                         	(38.4899, 39.503783, -88.804367, -87.503417)
        63997_Brownfield IL.gpx                                     	(36.863367, 37.914217, -89.326183, -87.995217)
        12729865_Buddy Holly - Rathbun Lake - MOGA 2012.gpx         	(40.669083, 41.2038, -93.33915, -92.406517)
        46611_Bushnell IL.gpx                                       	(40.176717, 40.919933, -90.98235, -90.014667)
        7447494_Cisco IL.gpx                                        	(39.816667, 40.1984, -88.943867, -88.444917)
        44394_Columbia MO.gpx                                       	(38.136467, 39.6926, -93.26765, -91.440317)
        7288725_Eureka MO.gpx                                       	(38.242983, 38.8305, -91.146717, -90.336433)
        12747791_Festus MO.gpx                                      	(37.869283, 38.58945, -90.80025, -89.961467)
        63996_Foosland IL.gpx                                       	(40.038317, 40.671367, -88.844517, -88.017583)
        44395_Fruit IL.gpx                                          	(38.390233, 39.30645, -90.492917, -89.334717)
        2434304_Griggsville IL.gpx                                  	(38.925317, 40.46425, -91.773667, -89.745583)
        10968825_MOGA 2013.gpx                                      	(39.0491, 39.786917, -89.277367, -88.322067)
        3502958_Mount Vernon IL.gpx                                 	(37.685667, 38.9526, -89.701733, -88.043467)
        3230890_Orchard Mines IL.gpx                                	(40.598067, 40.767967, -89.74365, -89.5265)
        3434583_Roanoke IL.gpx                                      	(40.531617, 41.06585, -89.5611, -88.83905)
        4055024_Rolla MO.gpx                                        	(37.191233, 38.708133, -92.73615, -90.816917)
        7443709_Shelby IL.gpx                                       	(38.856917, 39.7643, -89.482267, -88.332717)
        46564_Silva MO.gpx                                          	(36.55715, 37.973333, -91.222217, -89.459217)
        1180316_Springfield IL.gpx                                  	(39.323383, 40.28535, -90.2721, -89.00775)
        12745793_topo723 - Springfield IL.gpx                       	(39.323383, 39.80265, -89.70295, -89.294167)
        4046880_Trivol IL.gpx                                       	(40.509583, 40.872567, -90.12835, -89.663733)
        3219690_Tuscola IL.gpx                                      	(39.479117, 40.092221, -88.6626, -87.873083)
        2575620_Vanzant MO.gpx                                      	(36.273117, 37.579817, -93.059033, -91.442617)
        2465597_Wyoming IL.gpx                                      	(40.74445, 41.335483, -90.146167, -89.407733)
        Thu Jan 02 09:59:23 2014
        TOTAL TIME IN MINUTES: 0.271983333429

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

VERSION

    
"""

BASEDIR = r"C:\Users\Robert Oelschlaeger\AppData\Roaming\gsak\PQDownloads"

import sys
import os
import traceback
import optparse
import time

from simplekml import Kml
from quads import get_quad
from zipfile import ZipFile, is_zipfile
from kmldraw import kmldraw

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

DOCUMENT_NAME = "pqmap.kml"

def main (args, options):

    count = 0

    debug = options.debug

    kml = Kml()
    import datetime
    kml.document.name = "GPX Extent Map created by pqmap.py on %s" % datetime.date.today()

    for arg in args:

        assert os.path.isdir(arg), "%s is not a directory" % arg

        directory = arg
        files = os.listdir(arg)

        for zipfilename in files:

            pathname = os.path.join(directory, zipfilename)

            if is_zipfile(pathname):

                z = ZipFile(pathname, "r")

                for gpx_name in z.namelist():

                    if 'wpts' in gpx_name: 
                        continue

                    gpx = z.open(gpx_name, "r")

                    z.extract(gpx_name)
                    quad = get_quad(gpx)

                    if options.verbose:
                        print "%-60s\t%s" % (gpx_name, quad)
                    else:
                        print ".",

                    description = gpx_name
                    kmldraw(kml, description, quad)

                    count += 1

        break

    kml.save(DOCUMENT_NAME)
    if not options.verbose:
        print
    print "%d .gpx files processed" % count
    print "Output is in %s" % DOCUMENT_NAME

########################################################################

#   def get_quads(file_object):
#       lines = file_object.readlines()
#       print lines[:3]
#       return (0, 1, 2, 3)

########################################################################

if __name__ == '__main__':

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
                formatter=optparse.TitledHelpFormatter(),
                usage=globals()['__doc__'],
                version='$Id: py.tpl 332 2008-10-21 22:24:52Z root $')
        parser.add_option ('-v', '--verbose', action='store_true',
                default=False, help='verbose output')
        parser.add_option ('-d', '--debug', action='store_true',
                default=False, help='debug')
        (options, args) = parser.parse_args()
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if not args:
            args = [ BASEDIR ]
        if options.verbose: print time.asctime()
        exit_code = main(args, options)
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
