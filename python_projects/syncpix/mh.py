#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Tue 07 Jan 2014 12:04:26 PM CST
# Last Modified: Tue 07 Jan 2014 01:45:00 PM CST

"""
SYNOPSIS

    mh [-h] [-v,--verbose] [--version]

DESCRIPTION

    TODO This describes how to use this script.

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

########################################################################

import dominate
from dominate.tags import *
from itertools import groupby
from pprint import pprint

########################################################################

def mh(pixdir, route_name, results, debug=False):

    document = dominate.document()
    document.title = "Pictures from %s" % route_name

    groups = []
    uniquekeys = []

    # return gc
    def keyfunc(t): return t[2][1]

    # k is gcnumber
    for k, g in groupby(results, keyfunc):
        groups.append(list(g))
        uniquekeys.append(k)

    if debug:
        pprint(groups, sys.stderr, width=132)
        pprint(uniquekeys, sys.stderr, width=132)

    t = table(
            border=1, 
            cellpadding=3, 
            cellspacing=3,
            summary=route_name,
            align="center"
            )

    with t:

        # output the table caption
        caption(route_name)

        # output the table header
        tr(
            th("GC Name"), 
            th("Geocache Description"), 
            th("Imagefile")
            )
 
        for gcname_key, g in zip(uniquekeys, groups):

            # key gcname_key is gcname
            coord_info_url = "http://coord.info/%s" % gcname_key

            groups.append(list(g))
            uniquekeys.append(gcname_key)

            rowspan = len(g)
            first = True

            for time, filename, gc, tp in g:

                pathname = os.path.join(pixdir, filename)

                with tr(align="center"):

                    distance, gcnumber, description = gc
                    lat, lon = tp

                    if rowspan==1:
                        td( a(gcname_key, href=coord_info_url) )
                        td(description)
                    elif first:
                        td( a(gcname_key, href=coord_info_url), rowspan=rowspan)
                        td(description, rowspan=rowspan)
                        first = False

                    td( a(filename, href=pathname) )

    document += t

    print document

########################################################################

if __name__ == '__main__':

    import sys
    import os
    import traceback
    import optparse
    import time

    from results_table import results

    ########################################################################

    DATE = "20140104"
    PIXDIR = r"C:\Users\Robert Oelschlaeger\Google Drive\Caching Pictures\%s" % DATE
#   from syncpix import PIXDIR
    ROUTE_NAME = "topo727 - Cape Girardeau MO"

    ########################################################################

    def main ():

        global options, args

        mh(PIXDIR, ROUTE_NAME, results, options.debug)

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
                formatter=optparse.TitledHelpFormatter(),
                usage=globals()['__doc__'],
                version='$Id: py.tpl 332 2008-10-21 22:24:52Z root $')
        parser.add_option ('-v', '--verbose', action='store_true',
                default=False, help='verbose output')
        parser.add_option ('-d', '--debug', action='store_true',
                default=False, help='debug')
        (options, args) = parser.parse_args()
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.verbose: print time.asctime()
        exit_code = main()
        if exit_code is None:
            exit_code = 0
        if options.verbose: print time.asctime()
        if options.verbose: print 'TOTAL TIME IN MINUTES:',
        if options.verbose: print (time.time() - start_time) / 60.0
        sys.exit(exit_code)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

# vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
