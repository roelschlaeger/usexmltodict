#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Sun 23 Feb 2014 03:40:36 PM CST
# Last Modified: Mon 24 Feb 2014 10:03:17 AM CST

"""
SYNOPSIS

    clue [-h] [-v,--verbose] [--version]

DESCRIPTION

    This application computes and displays all solutions to the Clue geocache.

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

VERSION

"""

__VERSION__ = "0.0.1"

########################################################################

"""
The final cache is located at N 38 36.xxx w 92 1y.yzz.

    xxx is the number of the murderer.
    yy is the number of the weapon.
    zz is the number of the room in which the murder took place.

If you believe the murder suspect is:
    Professor Peter Plum, put 987 in the place where xxx is.
    Prince Philippe Azure, put 539 in the place where xxx is.
    Mrs. Patricia Peacock, put 292 in the place where xxx is.
    Mrs. Blanche White, put 666 in the place where xxx is.
    Miss Josephene Scarlet, put 357 in the place where xxx is.
    Lord Alfred Gray, put 762 in the place where xxx is.
    Reverend John Green, put 044 in the place where xxx is.
    Colonel Michael Mustard, put 123 in the place where xxx is.
    Lady Su Sian Lavender, put 424 in the place where xxx is.

If you believe that the murder room is:
    Ballroom, put 08 in the place where zz is.
    Hall, put 97 in the place where zz is.
    Lounge, put 86 in the place where zz is.
    Library, put 75 in the place where zz is.
    Kitchen, put 64 in the place where zz is.
    Study, put 53 in the place where zz is.
    Dining Room, put 42 in the place where zz is.
    Conservatory, put 31 in the place where zz is.
    Billiard Room, put 20 in the place where zz is.

If you believe that the murder weapon is:
    Revolver, put 79 in the place where yy is.
    Rope, put 78 in the place where yy is.
    Wrench, put 77 in the place where yy is.
    Pills, put 76 in the place where yy is.
    Lead Pipe, put 75 in the place where yy is.
    Knife, put 74 in the place where yy is.
    Candlestick, put 73 in the place where yy is.
"""

PERSONS = {
    "Azure": 539,
    "Gray": 762,
    "Green": 044,
    "Lavender": 424,
    "Mustard": 123,
    "Peacock": 292,
    "Plum": 987,
    "Scarlet": 357,
    "White": 666,
}

WEAPONS = {
    "Candlestick": 73,
    "Knife": 74,
    "Lead Pipe": 75,
    "Pills": 76,
    "Revolver": 79,
    "Rope": 78,
    "Wrench": 77,
}

ROOMS = {
    "Ballroom": 8,
    "Billiard Room": 20,
    "Conservatory": 31,
    "Dining Room": 42,
    "Hall": 97,
    "Kitchen": 64,
    "Library": 75,
    "Lounge": 86,
    "Study": 53,
}


########################################################################


def generate_locations():
    """generate all possible final locations based on PERSONS, WEAPONS and
ROOMS. Output is suitable for input to a spreadsheet program."""

    print "\t".join(["Person", "Weapon", "Room", "Latitude", "Longitude"])

    for person, xxx in PERSONS.items():
        for weapon, yy in WEAPONS.items():
            for room, zz in ROOMS.items():

                latstring = "N38 36.%s" % ("%03d" % xxx)
                y1, y2 = divmod(yy, 10)
                lonstring = "W92 1%d.%d%s" % (y1, y2, "%02d" % zz)

                print "\t".join([person, weapon, room, latstring, lonstring])

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

        generate_locations()

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
