#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 05 Jun 2014 12:16:26 PM CDT
# Last Modified: Thu 05 Jun 2014 12:44:31 PM CDT

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

import simplekml

########################################################################

OCALA_MIN = 34470
OCALA_MAX = 34483

ARDEN_ZIP = 19810


def lattodeg(s):
    """convert Ndd dd.ddd to float"""
    positive = s[0] == "N"
    s = s[1:]
    d, m = s.split()
    d = int(d)
    m, t = map(int, m.split('.'))
    deg = d + m / 60. + t / 60000.
    if not positive:
        deg = -deg
    print deg
    return deg


def lontodeg(s):
    """convert Wdd dd.ddd to float"""
    positive = s[0] == "E"
    s = s[1:]
    d, m = s.split()
    d = int(d)
    m, t = map(int, m.split('.'))
    deg = d + m / 60. + t / 60000.
    if not positive:
        deg = -deg
    print deg
    return deg


def process():
    """Process possible final cache locations"""

    kml = simplekml.Kml()

    lon = "W90 %02d.%03d" % divmod(ARDEN_ZIP, 1000)
    for ocala in range(OCALA_MIN, OCALA_MAX+1):
        name = "L%05d" % ocala
        lat = "N38 %02d.%03d" % divmod(ocala, 1000)
        print lat, lon
        dlat = lattodeg(lat)
        dlon = lontodeg(lon)
        print dlat, dlon
        coords = [(dlon, dlat)]
        kml.newpoint(name=name, coords=coords)
    kml.save("zipit_zippy.kml")

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
