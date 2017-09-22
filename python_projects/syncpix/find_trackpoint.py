#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Sat 01 Feb 2014 01:00:21 PM CST
# Last Modified: Tue 22 Aug 2017 10:26:29 AM CDT

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


def find_trackpoint(time, trackpoint_datetimes):
    """"
    Locates time in trackpoint_datetimes, returns (lat, lon) of corresponding
    location
    """

    # time is datetime
    # trackpoint_datetimes is list of (datetime, lat, lon)

    # NOTE: rlon and rlat are switched
    for rtime, rlon, rlat in trackpoint_datetimes:
        if rtime > time:
            return (rlat, rlon)
    print("Returning default")
    return (trackpoint_datetimes[0][2], trackpoint_datetimes[0][1])

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

        # TODO: Do something more interesting here...
        print('Hello world!')

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
            print(time.asctime())

        exit_code = main()

        if exit_code is None:
            exit_code = 0

        if options.verbose:
            print(time.asctime())
            print('TOTAL TIME IN MINUTES:',)
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

# end of file
