#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 05 Jun 2014 02:14:45 PM CDT
# Last Modified: Thu 05 Jun 2014 02:50:46 PM CDT

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

from pprint import pprint

"""
 3 A = Flowering Peach
 7 B = Pampas
 8 C = Firethorn - Yellow Jasmine
11 D = White Dogwood - Tea Olive - Camellia
 E = Holly - Golden Bell
 F = Pink Dogwood
 G = Golden Bell - Pink Dogwood - Camellia
 H = Juniper
 I = Flowering Peach * 2
 J = Magnolia


No. 1 Tea Olive
No. 2 Pink Dogwood
No. 3 Flowering Peach
No. 4 Flowering Crabapple
No. 5 Magnolia
No. 6 Juniper
No. 7 Pampas
No. 8 Yellow Jasmine
No. 9 Carolina Cherry
No. 10 Camellia
No. 11 White Dogwood
No. 12 Golden Bell
No. 13 Azalea
No. 14 Chinese Fir
No. 15 Fire Thorn
No. 16 Redbud
No. 17 Nandina
No. 18 Holly
"""

"""
 A = Flowering Peach
 B = Pampas
 C = Firethorn - Yellow Jasmine
 D = White Dogwood - Tea Olive - Camellia
 E = Holly - Golden Bell
 F = Pink Dogwood
 G = Golden Bell - Pink Dogwood - Camellia
 H = Juniper
 I = Flowering Peach * 2
 J = Magnolia

Final can be found at N38° AB.CDE W90° FG.HIJ
"""
ITEMS = {
    "Tea Olive": 1,
    "Pink Dogwood": 2,
    "Flowering Peach": 3,
    "Flowering Crabapple": 4,
    "Magnolia": 5,
    "Juniper": 6,
    "Pampas": 7,
    "Yellow Jasmine": 8,
    "Carolina Cherry": 9,
    "Camellia": 10,
    "White Dogwood": 11,
    "Golden Bell": 12,
    "Azalea": 13,
    "Chinese Fir": 14,
    "Firethorn": 15,
    "Redbud": 16,
    "Nandina": 17,
    "Holly": 18
}


def equate(s, e):
    print "%s %s" % (s, e)
    ops = e.split("-")
    for index, op in enumerate(ops):
        op = op.strip()
#       print op, ITEMS[op]
        if index == 0:
            v = ITEMS[op]
            continue
        v -= ITEMS[op]
    print "    %s = %d" % (s, v)
    globals()[s] = v


def process():
    equate("A", "Flowering Peach")
    equate("B", "Pampas")
    equate("C", "Firethorn - Yellow Jasmine")
    equate("D", "White Dogwood - Tea Olive - Camellia")
    equate("E", "Holly - Golden Bell")
    equate("F",  "Pink Dogwood")
    equate("G", "Golden Bell - Pink Dogwood - Camellia")
    equate("H", "Juniper")
    equate("I", "Flowering Peach")
#   print "*2"
    globals()["I"] *= 2
    equate("J", "Magnolia")
#   pprint(globals())
    print "Final can be found at \
N38 %(A)s%(B)s.%(C)s%(D)s%(E)s W90 %(F)s%(G)s.%(H)s%(I)s%(J)s" % globals()

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
