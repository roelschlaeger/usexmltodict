#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys

# Created:       Wed 01 Jan 2014 05:15:26 PM CST
# Last Modified: Tue 23 Feb 2016 12:16:07 PM CST

"""
SYNOPSIS

    kmldraw [-h] [-v,--verbose] [--version]

DESCRIPTION

    This script draws varying colors of rectangular areas using KML, with
    default output directed to kmldraw.kml.

EXAMPLES

    TODO: Show some examples of how to use this script.

    python kmldraw.py

EXIT STATUS

    TODO: List exit codes

AUTHOR

    : Robert L. Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

VERSION

    0.1.1

"""

from simplekml import Kml, PolyStyle

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


def luminance(r, g, b):
    # compute the luminance of an (r,g,b) color, where r, g, and b range from 0
    # to 10
    return ((0.2126 * r) + (0.7152 * g) + (0.0722 * b)) / 10.

########################################################################

# set the acceptable luminance values
MIN_LUMINANCE = 0.5
MAX_LUMINANCE = 0.95

# define a table of acceptable colors
COLOR_TABLE_DICT = {}

for rcolor in range(0, 16, 4):
    for gcolor in range(0, 16, 4):
        for bcolor in range(0, 16, 4):
            lum = luminance(rcolor, gcolor, bcolor)
            if MIN_LUMINANCE <= lum <= MAX_LUMINANCE:
                COLOR_TABLE_DICT[lum] = "80%c%c%c%c%c%c" % tuple(
                    hex(x)[-1] for x in [rcolor, rcolor, gcolor, gcolor, bcolor, bcolor]
                )

# COLOR_TABLE = [ COLOR_TABLE_DICT[ key ] for key in
# sorted(COLOR_TABLE_DICT.keys()) ]
COLOR_TABLE = [COLOR_TABLE_DICT[key] for key in sorted(COLOR_TABLE_DICT)]
del COLOR_TABLE_DICT


def colorgen():
    while 1:
        for value in COLOR_TABLE:
            yield value

########################################################################

NEXT_COLOR = colorgen()


def NextColor():
    """Return next sequential color from the generator"""
    if sys.version_info < (3,):
        return NEXT_COLOR.next()
    return next(NEXT_COLOR)

########################################################################


def kmldraw(kml, description, quad, name=None, color=None):

#   print(description, quad)
    minlat, maxlat, minlon, maxlon = quad

    pol = kml.newpolygon()
    pol.name = name or description
    pol.description = description
    pol.outerboundaryis = [
        (minlon, minlat),
        (maxlon, minlat),
        (maxlon, maxlat),
        (minlon, maxlat),
        (minlon, minlat)
    ]
    pol.polystyle = PolyStyle(color=color or NextColor())

########################################################################

if __name__ == '__main__':

#   import sys
    import os
    import traceback
    import optparse
    import time

    # this output was generated by pgmap.py
    RAWINPUT = """
                   12614439_B-2 Spirit -- Knob Noster MO.gpx	(38.096633, 39.376367, -94.342267, -92.779117)
                                    45606_Barnesville MO.gpx	(38.939, 40.845517, -93.740133, -91.329033)
                                         46563_Bogota IL.gpx	(38.4899, 39.503783, -88.804367, -87.503417)
                                     63997_Brownfield IL.gpx	(36.863367, 37.914217, -89.326183, -87.995217)
         12729865_Buddy Holly - Rathbun Lake - MOGA 2012.gpx	(40.669083, 41.2038, -93.33915, -92.406517)
                                       46611_Bushnell IL.gpx	(40.176717, 40.919933, -90.98235, -90.014667)
                                        7447494_Cisco IL.gpx	(39.816667, 40.1984, -88.943867, -88.444917)
                                       44394_Columbia MO.gpx	(38.136467, 39.6926, -93.26765, -91.440317)
                                       7288725_Eureka MO.gpx	(38.242983, 38.8305, -91.146717, -90.336433)
                                       63996_Foosland IL.gpx	(40.038317, 40.671367, -88.844517, -88.017583)
                                          44395_Fruit IL.gpx	(38.390233, 39.30645, -90.492917, -89.334717)
                                  2434304_Griggsville IL.gpx	(38.925317, 40.46425, -91.773667, -89.745583)
                                      10968825_MOGA 2013.gpx	(39.0491, 39.786917, -89.277367, -88.322067)
                                 3502958_Mount Vernon IL.gpx	(37.685667, 38.9526, -89.701733, -88.043467)
                                3230890_Orchard Mines IL.gpx	(40.598067, 40.767967, -89.74365, -89.5265)
                                      3434583_Roanoke IL.gpx	(40.531617, 41.06585, -89.5611, -88.83905)
                                        4055024_Rolla MO.gpx	(37.191233, 38.708133, -92.73615, -90.816917)
                                       7443709_Shelby IL.gpx	(38.856917, 39.7643, -89.482267, -88.332717)
                                          46564_Silva MO.gpx	(36.55715, 37.973333, -91.222217, -89.459217)
                                  1180316_Springfield IL.gpx	(39.323383, 40.28535, -90.2721, -89.005033)
                       12745793_topo723 - Springfield IL.gpx	(39.323383, 39.80265, -89.70295, -89.294167)
                                       4046880_Trivol IL.gpx	(40.509583, 40.872567, -90.12835, -89.663733)
                                      3219690_Tuscola IL.gpx	(39.479117, 40.092221, -88.6626, -87.873083)
                                      2575620_Vanzant MO.gpx	(36.273117, 37.579817, -93.059033, -91.442617)
                                      2465597_Wyoming IL.gpx	(40.74445, 41.335483, -90.146167, -89.407733)
"""

    DEFAULT_DOCUMENT_NAME = "kmldraw.kml"

    def add_patch(kml, lat, lon, extent, color):
        pol = kml.newpolygon()
        pol.name = color
        pol.description = color
        pol.outerboundaryis = [
            (lon, lat),
            (lon + extent, lat),
            (lon + extent, lat + extent),
            (lon, lat + extent),
            (lon, lat)
        ]
        pol.polystyle = PolyStyle(color=color)

    def create_color_map(color_list):
        kml = Kml()
        lat = 38.000
        init_lon = lon = -90.000
        extent = 0.02
        for index, color in enumerate(color_list):
            add_patch(kml, lat, lon, extent, color)
            lon += extent
            if (index % 10) == 9:
                lon = init_lon
                lat -= extent
        kml.save("color_patches.kml")
        print("Output in color_patches.kml")

    def main():

        global options, args

        if options.list_colors:
            create_color_map(COLOR_TABLE)
            sys.exit()

        output_filename = options.output

        kml = Kml()
        kml.document.name = "Test of kmldraw.py"

        for line in RAWINPUT[1:-1].split('\n'):
            text, quad = line.split("\t")
            name = text.strip()

            import re
            result = re.match(
                '\((\d+.\d+), (\d+.\d+), (-\d+.\d+), (-\d+.\d+)\)',
                quad
            )
            minlat, maxlat, minlon, maxlon = list(map(float, result.groups()))
            quad = (minlat, maxlat, minlon, maxlon)

            kmldraw(kml, name, quad)

        kml.save(output_filename)
        print("Wrote to: %s" % output_filename)

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version='$Id: py.tpl 332 2008-10-21 22:24:52Z root $')
        parser.add_option('-v', '--verbose', action='store_true',
                          default=False, help='verbose output')
        parser.add_option('-l', '--list', action='store_true',
                          dest="list_colors", default=False,
                          help='list colors and quit')
        parser.add_option('-o', '--output', action='store',
                          default=DEFAULT_DOCUMENT_NAME,
                          help='set output filename')
        (options, args) = parser.parse_args()
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.verbose:
            print(time.asctime())
        exit_code = main()
        if exit_code is None:
            exit_code = 0
        if options.verbose:
            print(time.asctime())
        if options.verbose:
            print('TOTAL TIME IN MINUTES:'),
        if options.verbose:
            print((time.time() - start_time) / 60.0)
        sys.exit(exit_code)
    except KeyboardInterrupt as e:      # Ctrl-C
        raise e
    except SystemExit as e:             # sys.exit()
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)

# vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
