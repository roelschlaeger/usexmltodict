#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Tue 22 Jul 2014 01:21:54 PM CDT
# Last Modified: Tue 09 Sep 2014 09:32:44 PM CDT

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

########################################################################

from dominate.tags import html, head, style, body, table, tr, th, td, hr, a
from dominate.tags import h3, h4
from time import asctime

PATH = "C:\Users\Robert Oelschlaeger\Desktop"
FILENAME = "Code_WaypointName_URL.csv"
DOCNAME = "topo765a - Saint Louis MO"
OUTFILE = "process.html"

import os.path

FILENAME = os.path.join(PATH, FILENAME)
from images import IMAGES
from notes import NOTES


def process():
#   doc = dominate.document(DOCNAME)

    h = html(name=DOCNAME)

    with h:

#           _head = head()

        _head = head()
        with _head:
            s = style()
            s.add("\nh3, h4 {text-align:center;}")
            s.add("\nth {background-color:yellow;}")
            s.add("\ntr, td, th {text-align:center;}")
            s.add("\ntd.left {text-align:left;}")
            s.add("\n")

        b = body()

        b.add(h3(DOCNAME))
        b.add(h4(asctime()))
        b.add(hr())

        t = table(border="1", cellpadding="3", cellspacing="3")
        b.add(t)

        r = tr()
        t.add(r)

        r.add(th("Code"))
        r.add(th("Waypoint"))
        r.add(th("Image"))
        r.add(th("Note"))

        f = open(FILENAME, "r")

        for index, line in enumerate(f.readlines()):
            if index == 0:
                continue

            code, waypoint_name, url = line.split('\t')

            r = tr()
            t.add(r)

            r.add(td(code))
            r.add(td(a(waypoint_name, href=url)))

            if code in IMAGES:
                link = IMAGES[code]
                if isinstance(link, type([])):
                    images = table()
                    for link in link:
                        r2 = tr()
                        r2.add(td(a(link, href=link)))
                        images.add(r2)
                else:
                    images = a(link, href=link)
            else:
                images = ""
            r.add(td(images))

            if code in NOTES:
                note = NOTES[code]
            else:
                note = "TBD"
            r.add(td(note, cls="left"))

    outfile = open(OUTFILE, "wb")
    print >> outfile, h
    outfile.close()
    print "Output is in %s" % OUTFILE

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
