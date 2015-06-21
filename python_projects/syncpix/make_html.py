#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Sun 05 Jan 2014 05:22:17 PM CST
# Last Modified: Sun 21 Jun 2015 02:19:57 PM CDT

"""
SYNOPSIS

    make_html [-h] [-v,--verbose] [--version]

DESCRIPTION

    Create an HTML file from the results

EXAMPLES

    python make_html.py > make_html.html

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

VERSION


"""

VERSION = "0.0.2"

########################################################################

import dominate
from dominate.tags import meta, style, table, \
    caption, tr, th, td, a
import os.path
from urllib import quote

########################################################################


def make_html(pixdir, route_name, results):

    title = "Pictures from %s" % route_name

    document = dominate.document(title=title)

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
        caption { background-color: #c0c040; font-size: 16px; \
font-family: "Courier New"; }
        body { font-size: 16px; }
        @media print {
            body { font-size: 8px; font-family: "Courier New" }
            caption { font-size: 10px }
            a {
            text-decoration: none; font-style: italic; font-weight: bold}
            th { background-color: white; color: black; }
        }
        """)

    with document.body:

        with table():

            caption(route_name)

            tr(
                th("Name"),
                th("Description"),
                th("Imagefile")
            )

            for time, filename, gc, tp in results:

                pathname = os.path.join(pixdir, filename)

                gcname, gcdesc = map(str, gc[1:])
                gclink = "http://coord.info/%s" % quote(gcname)

                with tr():

                    td(a(gcname, href=gclink))
                    td(gcdesc)
                    td(a(filename, href=quote(pathname)))

    print >>open("make_html.html", "w"), document

########################################################################

if __name__ == '__main__':

#   from datetime import tzinfo, datetime
#   from dateutil.tz import tzlocal
    from results_table import results

########################################################################

    import sys
    import os
    import traceback
    import optparse
    import time

    DATE = "20150619"
    HOME = r"C:\Users\Robert Oelschlaeger"
    PIXDIR = r"%s\Google Drive\Caching Pictures\%s" % (HOME, DATE)
    ROUTE_NAME = "topo803 - Springfield MO"

    def main():

        global options, args

        make_html(PIXDIR, ROUTE_NAME, results)

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version='$Id: make_html.py %s' % VERSION)
        parser.add_option('-v', '--verbose', action='store_true',
                          default=False, help='verbose output')
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
    except KeyboardInterrupt, e:  # Ctrl-C
        raise e
    except SystemExit, e:  # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

# vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
