#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python
# -*- encoding=utf-8 -*-
# Created:       Sun 08 Feb 2015 12:00:50 PM CST
# Last Modified: Sun 08 Feb 2015 12:56:52 PM CST

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

# zip codes for Palm Coast, FL
# http://www.zip-codes.com/city/FL-PALM-COAST.asp
PALM_COAST_FL = [
    32135,
    32137,
    32142,
    32143,
    32164
]

APPLETON_WI = [
    54911,
    54912,
    54913,
    54914,
    54915,
    54919
]


def convert(s):
    """convert ADD DD.DDD latitude/longitude string to float"""
    print s,
    s, rest = s[0], s[1:]
#   print s, rest
    sign = ((s == 'W') or (s == 'S'))
#   print sign
    sdeg, smin = map(float, rest.split())
    angle = sdeg + smin / 60.0
    if sign:
        angle = -angle
    print angle
    return angle

from simplekml import Kml


def process(args, options):

    kml = Kml()
    kml.newpoint(
        name="GC3DQM3 zip-a-dee-doo-dah N36_55.979 W090_34.064",
        coords=[(-90.56773, 36.93298)]
    )

    for lat in PALM_COAST_FL:

        latitude = convert("N36 %2d.%03d" % (divmod(lat, 1000)))

        for lon in APPLETON_WI:

            longitude = convert("W90 %2d.%03d" % (divmod(lon, 1000)))
            name = "%s_%s" % (lat, lon)

            kml.newpoint(name=name, coords=[(longitude, latitude)])

    kml.save('zip_a_dee_doo_dah.kml')

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

        global OPTIONS, ARGS

        process(ARGS, OPTIONS)

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
