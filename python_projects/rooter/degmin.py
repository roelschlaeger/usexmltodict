#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Fri 17 Jan 2014 06:11:21 PM CST
# Last Modified: Fri 17 Jan 2014 06:16:01 PM CST

"""
SYNOPSIS

    TODO degmin [-h] [-v,--verbose] [--version]

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

from math import trunc


def degmin(latlon, posneg=" -"):
    """
    Convert a latitude or longitude in 'latlon' to a proper string formatted
    like N12 34.567 using posneg[0] as the positive value indicator, posneg[1]
    as the negative value indicator.

    For latitude,  string = degmin(lat, "NS")
    For longitude, string = degmin(lon, "EW")

    """

    v = float(latlon)

    sign = (v < 0)

    v = abs(v)

    degrees, fraction = trunc(v), v - trunc(v)
    minutes = fraction * 60.
    minutes, thousandths = (
        trunc(minutes),
        trunc((minutes - trunc(minutes)) * 1000.)
    )

    # apply sign
    if sign:
        s = posneg[1]
    else:
        s = posneg[0]

    s = s.strip()
    s += "%d %02d.%03d" % (degrees, minutes, thousandths)

    return s

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

        print degmin(38.5, "NS")
        print degmin(-90, "EW")

########################################################################

    try:
        start_time = time.time()

        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version=__VERSION__
        )

        parser.add_option(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        (options, args) = parser.parse_args()

        #   if len(args) < 1:
        #       parser.error ('missing argument')

        if options.verbose:
            print time.asctime()

        exit_code = main()

        if exit_code is None:
            exit_code = 0

        if options.verbose:
            print time.asctime()
            print 'TOTAL TIME IN MINUTES:',
            print (time.time() - start_time) / 60.0

        sys.exit(exit_code)

    except KeyboardInterrupt, e:        # Ctrl-C
        raise e

    except SystemExit, e:               # sys.exit()
        raise e

    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

# end of file
