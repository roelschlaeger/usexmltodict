#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Tue 07 Jan 2014 12:04:26 PM CST
# Last Modified: Mon 22 Jun 2015 02:22:45 PM CDT

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
from dominate.tags import meta, style, table, caption, tr, th, td, a
from itertools import groupby
from pprint import pprint
import os.path

########################################################################


def make_html(pixdir, route_name, results, debug=False):

    document = dominate.document(
        title="Pictures from %s" % route_name,
    )

    with document.head:
        meta(charset="UTF-8")
        style("""
            table { page-break-inside:auto; border-spacing:3px; padding:3px; }
            table { margin-left:auto; margin-right:auto; }
            table, td, th, tr { border:1px solid green; }
            th { background-color: green; color: white; }
            th.tiny { width:3%; }
            th.narrow { width:47%; }
            th.wide { width:50%; }
            tr { page-break-inside:avoid; page-break-after:auto; }
            tr.center { margin-left:auto; margin-right:auto; }
            tr.alt { background-color: #f0f0f0; }
            caption { background-color: #c0c040; \
font-size: 16px; \
font-family: "Courier New"; }
            td.center { text-align: center }
            body { font-size: 16px; }
            @media print {
                body { font-size: 8px; font-family: "Courier New" }
                caption { font-size: 10px }
                a {
                  text-decoration: none; font-style: italic; font-weight: bold
                }
                th { background-color: white; color: black; }
            }
        """)

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

    picture_table = table()
    picture_table.add(caption(route_name))
    with picture_table:

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

                with tr():

                    distance, gcnumber, description = gc
                    lat, lon = tp

                    if rowspan == 1:
                        td(a(gcname_key, href=coord_info_url, target="_blank"))
                        td(description or "", cls="center")
                    elif first:
                        td(
                            a(gcname_key, href=coord_info_url,
                              target="_blank"),
                            rowspan=rowspan
                        )
                        td(description or "", rowspan=rowspan, cls="center")
                        first = False

                    td(a(filename, href=filename, target="_blank"))

    document += picture_table

    outfilename = os.path.join(pixdir, "make_html.html")
    print >> open(outfilename, "w"), unicode(document).encode('utf-8')
    print "Output is in %s" % outfilename

########################################################################

if __name__ == '__main__':

    import sys
    import os
    import traceback
    import optparse
    import time

    ########################################################################

    DATE = "20150619"
    HOME = r"C:\Users\Robert Oelschlaeger"
    PIXDIR = r"%s\Google Drive\Caching Pictures\%s" % (HOME, DATE)
    PIXDIR = "."
    ROUTE_NAME = "topo803 - Springfield IL"

    ########################################################################

    def main():

        global options, args

        import pickle
        closest_waypoints = pickle.Unpickler(
            open("closest_waypoints.dmp")
        ).load()
        from pprint import pprint
        pprint(closest_waypoints)

        make_html(PIXDIR, ROUTE_NAME, closest_waypoints, options.debug)

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
