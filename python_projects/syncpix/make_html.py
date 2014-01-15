#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Sun 05 Jan 2014 05:22:17 PM CST
# Last Modified: Tue 07 Jan 2014 04:12:23 PM CST

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

# from pexpect import run, spawn

# Uncomment the following section if you want readline history support.
#import readline, atexit
#histfile = os.path.join(os.environ['HOME'], '.TODO_history')
#try:
#    readline.read_history_file(histfile)
#except IOError:
#    pass
#atexit.register(readline.write_history_file, histfile)

########################################################################

from dominate.tags import *
import os.path

########################################################################

def make_html(pixdir, route_name, results):

    title = "Pictures from %s" % route_name

    document = html( title=title )
    with document:
        head()
        with body(footer=title):

            with table(
                    border="1", 
                    cellspacing="3", 
                    cellpadding="3", 
                    summary=route_name, 
                    align="center"
                    ):

                caption(route_name)

                tr(
                    th("Name"), 
                    th("Description"), 
                    th("Imagefile")
                    )

                for time, filename, gc, tp in results:

                    pathname = os.path.join(pixdir, filename)

                    gcname, gcdesc = map(str, gc[1:])
                    gclink = "http://coord.info/%s" % gcname

                    with tr(align="center"):

                        td( a(gcname, href=gclink) )
                        td( gcdesc )
                        td( a(filename, href=pathname) )

    print >>open("make_html.html", "w"), document

########################################################################

if __name__ == '__main__':

    from datetime import tzinfo, datetime
    from dateutil.tz import tzlocal
    from results_table import results

########################################################################

    import sys
    import os
    import traceback
    import optparse
    import time

    DATE = "20140104"
    PIXDIR = r"C:\Users\Robert Oelschlaeger\Google Drive\Caching Pictures\%s" % DATE
#   from syncpix import PIXDIR
    ROUTE_NAME = "topo727 - Cape Girardeau MO"

    def main ():

        global options, args

        make_html(PIXDIR, ROUTE_NAME, results)

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
                formatter=optparse.TitledHelpFormatter(),
                usage=globals()['__doc__'],
                version='$Id: py.tpl 332 2008-10-21 22:24:52Z root $')
        parser.add_option ('-v', '--verbose', action='store_true',
                default=False, help='verbose output')
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
