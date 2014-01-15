#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Tue 07 Jan 2014 12:04:26 PM CST
# Last Modified: Wed 15 Jan 2014 04:08:02 PM CST

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

__VERSION__ = "0.0.1"

import dominate
from dominate.tags import table, caption, tr, th, td, a
from itertools import groupby
from pprint import pprint
import os.path

########################################################################


def make_html(pixdir, route_name, results, debug=False):

    document = dominate.document()
    document.title = "Pictures from %s" % route_name

    groups = []
    uniquekeys = []

    # return gcname from line in results
    def keyfunc(t):
        return t[2][1]

    # k is gcnumber
    for k, g in groupby(results, keyfunc):
        groups.append(list(g))
        uniquekeys.append(k)

    if debug:
        pprint(groups, sys.stderr, width=132)
        pprint(uniquekeys, sys.stderr, width=132)

    picture_table = table(
        border=1,
        cellpadding=3,
        cellspacing=3,
        summary=route_name,
        align="center"
    )

    with picture_table:

        # output the table caption
        caption(route_name)

        # output the table header
        tr(
            th("GC Name"),
            th("Geocache Description"),
            th("Imagefile")
        )

        # group output fows by gcname_key
        for gcname_key, g in zip(uniquekeys, groups):

            # key gcname_key is gcname
            coord_info_url = "http://coord.info/%s" % gcname_key

#           groups.append(list(g))
#           uniquekeys.append(gcname_key)

            rowspan = len(g)
            first = True

            for time, filename, gc, tp in g:

                pathname = os.path.join(pixdir, filename)

                with tr(align="center"):

                    distance, gcnumber, description = gc
                    lat, lon = tp

                    if rowspan == 1:
                        td(a(gcname_key, href=coord_info_url))
                        td(description or "")
                    elif first:
                        td(a(gcname_key, href=coord_info_url), rowspan=rowspan)
                        td(description or "", rowspan=rowspan)
                        first = False

                    td(a(filename, href=pathname))

    document += picture_table

    outfilename = os.path.join(pixdir, "make_html.html")
    print >> open(outfilename, "w"), document
    print "Output is in %s" % outfilename

########################################################################

if __name__ == '__main__':

    import sys
    import os
    import traceback
    import optparse
    import time

    from results_table import results

    ########################################################################

    DATE = "20140111"
    HOME = r"C:\Users\Robert Oelschlaeger"
    PIXDIR = r"%s\Google Drive\Caching Pictures\%s" % (HOME, DATE)
    ROUTE_NAME = "topo730 - Sikeston MO"

    ########################################################################

    def main():

        global options, args

        make_html(PIXDIR, ROUTE_NAME, results, options.debug)

    ########################################################################

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version=__VERSION__)
        parser.add_option('-v',
                          '--verbose',
                          action='store_true',
                          default=False,
                          help='verbose output'
                          )
        parser.add_option('-d',
                          '--debug',
                          action='store_true',
                          default=False,
                          help='debug'
                          )
        (options, args) = parser.parse_args()
        #if len(args) < 1:
        #    parser.error ('missing argument')
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
