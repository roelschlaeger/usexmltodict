#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Sat 04 Jul 2015 10:04:51 AM CDT
# Last Modified: Sat 04 Jul 2015 11:40:18 AM CDT

"""
SYNOPSIS

    TODO helloworld [-h | --help] [-v | --version] [--verbose]

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

SUSPECTS = (
    ("Reverend John Green", 44),
    ("Colonel Michael Mustard", 123),
    ("Mrs. Patricia Peacock", 292),
    ("Miss Josephene Scarlet", 357),
    ("Lady Su Sian Lavender", 424),
    ("Prince Philippe Azure", 539),
    ("Mrs. Blanche White", 666),
    ("Lord Alfred Gray", 762),
    ("Professor Peter Plum", 987)
)

ROOMS = (
    ("Ballroom", 8),
    ("Billiard Room", 20),
    ("Conservatory", 31),
    ("Dining Room", 42),
    ("Study", 53),
    ("Kitchen", 64),
    ("Library", 75),
    ("Lounge", 86),
    ("Hall", 97)
)

WEAPONS = (
    ("Candlestick", 73),
    ("Knife", 74),
    ("Lead Pipe", 75),
    ("Pills", 76),
    ("Wrench", 77),
    ("Rope", 78),
    ("Revolver", 79)
)


import simplekml


def convert(s):
    hemi = s[0]
    d, m = map(float, s[1:].split())
    if (hemi == 'S' or hemi == 'W'):
        return -(d + m / 60.000)
    return (d + m / 60.000)

# print convert("N38 42.123")
# print convert("W90 12.345")
# import sys
# sys.exit(1)


def process():
    """Compute possible final coordinates"""
    kml = simplekml.Kml()
#   index = 0
    for suspect_info in SUSPECTS:
        suspect, xxx = suspect_info
        suspect_folder = kml.newfolder(name=suspect)

        for weapon_info in WEAPONS:
            weapon, yy = weapon_info
            folder = suspect_folder.newfolder(name=weapon)

            for room_info in ROOMS:
                room, zz = room_info
                final = "N38 36.%s/W92 1%s%s" % (
                    xxx,
                    "%s.%s" % (divmod(yy, 10)),
                    zz
                )
                lat, lon = map(convert, final.split("/"))
#               print suspect_info, room_info, weapon_info, final
                name = "%s: %s: %s" % (suspect, weapon, room)
                description = "%s %s %s" % (suspect, weapon, room)
                folder.newpoint(
                    name=name,
                    description=description,
                    coords=[(lon, lat)]
                )
#               index += 1
    kml.save("clue_game.kml")


if __name__ == '__main__':

    import argparse
    import os
    import sys
    import textwrap
    import time
    import traceback

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

        global OPTIONS

        process()

########################################################################

    try:
        START_TIME = time.time()

        PARSER = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage=textwrap.dedent(globals()['__doc__']),
            version="Version: %s" % __VERSION__
        )

        PARSER.add_argument(
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        OPTIONS = PARSER.parse_args()

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
