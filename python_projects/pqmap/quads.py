#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Wed 01 Jan 2014 04:16:58 PM CST
# Last Modified: Mon 13 Jan 2014 07:21:39 PM CST

"""
SYNOPSIS

    TODO quads [-h] [-v,--verbose] [--version] [-d --debug]

DESCRIPTION

    TODO This describes how to use this script.
    This docstring will be printed by the script if there is an error or
    if the user requests help (-h or --help).

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Name <name@example.org>

LICENSE

    This script is in the public domain.

VERSION


"""

# Uncomment the following section if you want readline history support.
#import readline, atexit
#histfile = os.path.join(os.environ['HOME'], '.TODO_history')
#try:
#    readline.read_history_file(histfile)
#except IOError:
#    pass
#atexit.register(readline.write_history_file, histfile)

import xml.etree.ElementTree as ET

########################################################################

BASE_TAG = '{http://www.topografix.com/GPX/1/0}'


def TAG(s):
    return BASE_TAG + s

ROOT_TAG = TAG('gpx')
BOUNDS_TAG = TAG('bounds')

########################################################################

# from pprint import pprint


def get_quad(file_object, debug=False):

    result = (0, 0, 0, 0)
    tree = ET.parse(file_object)
    root = tree.getroot()
    assert root.tag == ROOT_TAG, "Unexpected root tag: %s != %s" % (root.tag, ROOT_TAG)

    bounds = root.find(BOUNDS_TAG)

    if debug:
        print bounds
        print dir(bounds)
        print bounds.items()

    minlat = bounds.attrib["minlat"]
    maxlat = bounds.attrib["maxlat"]
    minlon = bounds.attrib["minlon"]
    maxlon = bounds.attrib["maxlon"]
#   print minlat, maxlat, minlon, maxlon

    result = tuple(map(float, [minlat, maxlat, minlon, maxlon]))
    return result

########################################################################

if __name__ == '__main__':

#   from pexpect import run, spawn

    import sys
    import os
    import traceback
    import optparse
    import time

    def main():

        global options, args

        debug = options.debug

        for filename in args:

            file_object = open(filename, "r")

            print "filename: %s" % filename
            print get_quad(file_object, debug)

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version='$Id: py.tpl 332 2008-10-21 22:24:52Z root $')
        parser.add_option('-v', '--verbose', action='store_true',
                          default=False, help='verbose output')
        parser.add_option('-d', '--debug', action='store_true', default=False,
                          help='debug output')
        (options, args) = parser.parse_args()

        if not args:
            args = ["1180316_Springfield IL.gpx"]

        if options.verbose:
            print time.asctime()
        exit_code = main()
        if exit_code is None:
            exit_code = 0
        if options.verbose:
            print time.asctime()
        if options.verbose:
            print 'TOTAL TIME IN MINUTES:',
        if options.verbose:
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

# vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
