#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Tue 10 Jun 2014 09:12:52 AM CDT
# Last Modified: Tue 10 Jun 2014 04:51:45 PM CDT

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

import codecs
import csv
from csv import DictReader
from gpxpy.gpx import GPX
from gpxpy.gpx import GPXWaypoint as GSAKWaypoint
# from gsak import GSAKWaypoint

OUTFILENAME = "cake.gpx"
FILENAME = "6-10 Cakeway to the West Installed Locations.txt"
#   [
#       'GPS',
#       'Site',
#       'Street Address',
#       'City',
#       'ST',
#       'Zip',
#       'Location on Site',
#       'First Screen'
#   ]


def process():

    print csv.list_dialects()
    dr = DictReader(
        codecs.open(
            FILENAME,
            "rb",
            "utf-8",
            "ignore"
        ),
        dialect='excel-tab'
    )
#   lines = open(FILENAME).readlines()
#   print len(lines)
#   print lines[0]
#   print lines[1]
    print dr.fieldnames

    waypoints = []
    for index, row in enumerate(dr):

        def fixup_row(key):
            t = row[key]
#           t = t.replace(chr(0x92), "'")
#           t = t.replace(chr(0x93), '"')
#           t = t.replace(chr(0x94), '"')
#           t = t.replace(chr(0x95), "-")
#           t = t.replace(chr(0xA0), " ")
            return t

        name = u"STL%03d" % index
#       name = fixup_row('Site')

#       Code = u"STL%03d" % index

        description = fixup_row('Site')

        latlon = row['GPS']
        if latlon:
            lat, lon = latlon.split()
        else:
            lat, lon = (0.0, 0.0)

        comment = u"; ".join([
            fixup_row('Location on Site'),
            fixup_row('First Screen'),
            fixup_row('Street Address'),
            fixup_row('City'),
            fixup_row('ST'),
            fixup_row('Zip'),
        ])

        waypoint = GSAKWaypoint(
            lat,
            lon,
            name=name,
            description=description,
            comment=comment,
            type="Geocache|Unknown Cache",
#           Code=Code
        )
#       print repr(waypoint)

        waypoints.append(waypoint)

    # create the gpx file
    gpx = GPX(waypoints)
    gpx.author = "Robert L. Oelschlaeger"
    gpx.email = "roelschlaeger@gmail.com"
    gpx.creator = "cake.py"
    gpx.description = "Location of St. Louis 250th Birthday Celebration cakes"

    # write it
    outfile = codecs.open(OUTFILENAME, "wb", "utf-8", "replace")
#   print dir(outfile)
    outfile.write(gpx.to_xml())
    outfile.close()

    # tell user
    print "output is in %s" % OUTFILENAME

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
