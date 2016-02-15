#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Sat 13 Feb 2016 02:15:52 PM CST
# Last Modified: Sat 13 Feb 2016 02:34:44 PM CST

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

from xml.etree import ElementTree as ET
from LatLon23 import Latitude, LatLon, Longitude
from pprint import pprint

FNAME = 'topo833b - Perry County IL.gpx'
# LL_FORMAT = 'D'  # just degrees
LL_FORMAT = 'H%d% %M'  # hemisphere, integer degrees and minutes

def get_wpts(fname):
    tree = ET.parse(fname)
    root = tree.getroot()
    wpt_tag = root.tag.replace('gpx', 'wpt')
    wpts = root.findall(wpt_tag)
    return wpts


def job():
    wpts = get_wpts(FNAME)

    for index, w in enumerate(wpts):
        if index == 0:
            pprint(dir(w))
            print()
            pprint(list(w))
            print()
        lat = Latitude(w.get('lat'))
        lon = Longitude(w.get('lon'))
        name = w[1].text  # w.get('name')
        desc = w[2].text  # w.get('desc')
        print(name, desc, lat.to_string(LL_FORMAT), lon.to_string(LL_FORMAT))  # , lat, lon)
        for itemindex, item in enumerate(w.getchildren()):
            print itemindex, item.tag, ':', item.text
            if itemindex == 6:
                for elemindex, elem in enumerate(item):
                    print "\t", elemindex, elem.tag, ':', elem.text
                    if elemindex == 0:
                        for extindex, wpt_extension in enumerate(elem):
                            print "\t\t", extindex, wpt_extension.tag, ':', wpt_extension.text
                    if elemindex == 1:
                        for cacheindex, cache in enumerate(elem):
                            print "\t\t", cacheindex, cache.tag, ':', cache.text
        if index > 1:
            break
#   pprint(wpts)


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

        job()
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
