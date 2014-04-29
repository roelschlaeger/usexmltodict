#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Tue 29 Apr 2014 04:24:08 PM CDT
# Last Modified: Tue 29 Apr 2014 05:41:06 PM CDT

"""
SYNOPSIS

    louis [-h] [-v,--verbose] [--version]

DESCRIPTION

    This script computes values for certification of the
    "Nothing to L.O.U.I.S. Challenge"
    http://www.geocaching.com/geocache/GC4H5VZ_nothing-to-l-o-u-i-s-challenge
    ?guid=19f1a3ae-192a-46a0-9317-76ad28777859

    Input data is contained in the file "390613.gpx"

EXAMPLES

    python louis.py

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

VERSION

"""

__VERSION__ = "0.0.3"

########################################################################

from xml.etree import ElementTree as ET
from collections import Counter, defaultdict

########################################################################

FILENAME = "390613.gpx"
"""The filename being read; contains found cache information"""

########################################################################


def get_first_gc(gc_namelist, three_letter_namelist):
    """Locate the lexicographically first cache for each element in
three_letter_namelist"""

    first_gc_dict = defaultdict(None)

    for three_letter_name, gc_name in zip(three_letter_namelist, gc_namelist):
        if first_gc_dict.get(three_letter_name) is None:
            first_gc_dict[three_letter_name] = gc_name
        elif len(first_gc_dict[three_letter_name]) > len(gc_name):
            first_gc_dict[three_letter_name] = gc_name
        elif first_gc_dict[three_letter_name] > gc_name:
            first_gc_dict[three_letter_name] = gc_name

    return first_gc_dict

########################################################################


def process(filename):
    """Get counts of the number of GCx files that have been found on a
per-state basis"""

    print __VERSION__
    print "Reading from %s" % filename

    tree = ET.parse(filename)
    root = tree.getroot()
    wpts = root.findall(root.tag.replace("gpx", "wpt"))
    print "%d geocaches processed" % len(wpts)

    # get all of the GC names
    raw_gc = [w[1].text for w in wpts]

    # get all of the states
    raw_states = [w[7][9].text for w in wpts]

    # get the first three letters of each GC name for Illinois and Missouri
    tlc = ["%s_%s" % (st, x[:3])
           for x, st in zip(raw_gc, raw_states)
           if st in ["Illinois", "Missouri"]
           ]

    # get GC names for Illinois and Missouri
    gc = [x for x, st in zip(raw_gc, raw_states)
          if st in ["Illinois", "Missouri"]
          ]

    # count them up
    c = Counter(tlc)

    # print the result
    result = sorted(c.keys())
    print "%d results" % len(result)

    # show the sorted counts for each key
    print "%s\t%s" % ("key", "length")
    for k in sorted(c.keys()):
        print "%s\t%s" % (k, c[k])
    print

    # show the first GC for each key
    result = get_first_gc(gc, tlc)
    print "%s\t%s" % ("key", "GC")
    for k in sorted(result.keys()):
        print "%s\t%s" % (k, result[k])

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

        process(FILENAME)

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
