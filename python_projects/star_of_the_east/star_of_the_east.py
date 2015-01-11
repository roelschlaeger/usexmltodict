#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Sun 11 Jan 2015 04:53:43 PM CST
# Last Modified: Sun 11 Jan 2015 05:11:49 PM CST

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

from simplekml import Kml

def convert(s):
    sign = s[0]
    deg = float(s[1:3])
    sec = float(s[4:]) / 60.
    result = deg + sec
    if sign == "S" or sign == "W":
        result = -result
    return result

def process():
    kml = Kml()
    for a in range(10):
        for b in range(10):
            for c in range(10):
                if c == 0:
                    continue
                q, r = divmod(a + b, c)
                if r:
                    continue
#               print a, b, c, q + 564, a * b * c + 87
                name = "Star_%d_%d_%d" % (a, b, c)
                lat = convert("N38 26.%03d" % (q + 564))
                lon = convert("W91 00.%03d" % (a * b * c + 87))
                coords = [(lon, lat)]
                print a, b, c, lat, lon
                kml.newpoint(name=name, coords=coords)
    kml.save("star_of_the_east.kml")

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

#       # TODO: Do something more interesting here...
#       print 'Hello world!'

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
