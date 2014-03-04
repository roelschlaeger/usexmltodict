#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# -*- coding: XXX-8 -*-

# Created:       Tue 04 Mar 2014 12:52:05 PM CST
# Last Modified: Tue 04 Mar 2014 05:50:11 PM CST

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

FILENAME = "myfinds.gpx"

########################################################################

import codecs
from xml.etree import ElementTree as ET

import csv

# from pprint import pprint

########################################################################

# <?xml version="1.0" encoding="utf-8"?>
# <gpx xmlns:xsd="http://www.w3.org/2001/XMLSchema"
# xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
# version="1.1" creator="GSAK"
# xsi:schemaLocation="http://www.topografix.com/GPX/1/1
# http://www.topografix.com/GPX/1/1/gpx.xsd
# http://www.groundspeak.com/cache/1/0/1
# http://www.groundspeak.com/cache/1/0/1/cache.xsd http://www.gsak.net/xmlv1/6
# http://www.gsak.net/xmlv1/6/gsak.xsd"
# xmlns="http://www.topografix.com/GPX/1/1">

########################################################################


def process_file(filename):

    tree = ET.parse(filename)

    root = tree.getroot()
    wpts = root.findall(root.tag.replace("gpx", "wpt"))

    w0 = wpts[0]

    exttag = w0.tag.replace("wpt", "extensions")

    nametag = w0.tag.replace("wpt", "name")
    gcnames = [w.find(nametag).text or "None" for w in wpts]

    desctag = w0.tag.replace("wpt", "desc")
    descriptions = [
        (w.find(desctag).text or "None").encode('ascii', 'replace')
        for w in wpts
    ]

    extensions = [w.find(exttag) for w in wpts]

    ext0 = extensions[0]

    e0 = ext0[0]
    e1 = ext0[1]

    statetag = e1[0].tag.replace("name", "state")

    states = [
        (e[1].find(statetag).text or "None").encode('ascii', 'replace')
        for e in extensions
    ]

    countytag = e0[0].tag.replace("UserFlag", "County")

    counties = [
        (e[0].find(countytag).text or "None").encode('ascii', 'replace')
        for e in extensions
    ]

    datetag = e0[0].tag.replace("UserFlag", "UserFound")

    dates = [e[0].find(datetag).text or "None" for e in extensions]

    database = zip(dates, states, counties, gcnames, descriptions)

    OUTFILENAME = "outfile.xls"
    outfile = open(OUTFILENAME, "w")
    writer = csv.writer(outfile)

    row = "\t".join(
        [
            "Date",
            "State",
            "County",
            "GC",
            "Description"
        ]
    )
    row = row.encode('ascii', 'replace')
    writer.writerow(row)

    for data in database:

        row = "\t".join(data)
        row = row.encode('ascii', 'replace')
        writer.writerow(row)

    outfile.close()

    print "%s is the output file" % OUTFILENAME

##########u##############################################################

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

        process_file(FILENAME)

########################################################################

    try:
        start_time = time.time()

        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version=__VERSION__
        )

        parser.add_option(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        (options, args) = parser.parse_args()

        #   if len(args) < 1:
        #       parser.error ('missing argument')

        if options.verbose:
            print time.asctime()

        exit_code = main()

        if exit_code is None:
            exit_code = 0

        if options.verbose:
            print time.asctime()
            print 'TOTAL TIME IN MINUTES:',
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

# end of file
