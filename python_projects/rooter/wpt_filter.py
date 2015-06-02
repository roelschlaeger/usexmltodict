#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Wed 08 Jan 2014 10:18:57 AM CST
# Last Modified: Wed 08 Jan 2014 12:09:12 PM CST

"""
SYNOPSIS

    wpt_filter [-h] [-v,--verbose] [--version] [-d, --debug] { filename }

DESCRIPTION

    Filter waypoints from a route to remove User2 == "SKIP" values in
    preparation for building a Google Earth route

EXAMPLES

    wpt_filter # operates on "default.gpx"

    wpt_filter filename # operates on "filename"

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

"""

__VERSION__ = "0.1.0"

########################################################################

from pprint import pprint
from xml.etree import ElementTree as ET

NAMETAG = None                  # replaced later

#######################################################################

def apply_wpts_filter(wpts, debug=False):

    extensionstag = wpts[0].tag.replace("wpt", "extensions")
    if debug:
        print "extensionstag: %s" % extensionstag

    extensions = [w.find(extensionstag) for w in wpts]

    wptExtensionTag = extensions[0][0].tag
    if debug:
        print "wptExtensionTag: %s" % wptExtensionTag

    wpt_extensions = [e.find(wptExtensionTag) for e in extensions]
    if debug:
        print "wpt_extensions"
        pprint(wpt_extensions)
        print

    u2tag = wpt_extensions[0][0].tag.replace("UserFlag", "User2")
    if debug:
        print "u2tag: %s" % u2tag

    user2 = [w.find(u2tag) for w in wpt_extensions]
    if debug:
        print "user2"
        pprint(user2)
        print

    filtered_wpts = [w for (w, u) in zip(wpts, user2) if (u is None) or (u.text != "SKIP")]

    return filtered_wpts

########################################################################

if __name__ == '__main__':

    import sys
    import os
    import traceback
    import optparse
    import time

    ########################################################################

    def get_wpts(filename, debug=False):
        """Retrieve waypoints from filename"""

        tree = ET.parse(filename)
        root = tree.getroot()

        if debug:
            print "Metadata:" 
            metadata = root.find(root.tag.replace("gpx", "metadata"))
            for item in metadata:
                if (item.text is not None) and (item.text.strip()):
                    print "%s: %s" % (item.tag, item.text)
            print

        # this is needed by printnames in command line test
        global NAMETAG
        NAMETAG = root.tag.replace("gpx", "name")

        _wpttag = root.tag.replace("gpx", "wpt")
        wpts = root.findall(_wpttag)

        return wpts

    ########################################################################

    def printnames(wpts):
        """Print the names of the waypoints in wpts"""

#       global NAMETAG
        for item in wpts:
            name = item.find(NAMETAG).text
            print name
        print

    ########################################################################

    def main(args, options):

        debug = options.debug

        if debug:
            pprint(options)
            pprint(args)

        filename = (args and args[0]) or "default.gpx"
        if debug:
            print filename

        wpts = get_wpts(filename, debug)

        if debug:
            print "wpts"
            print len(wpts)
            printnames(wpts)
#           pprint(wpts, width=132)
            print

        filtered_wpts = apply_wpts_filter(wpts)
        if debug:
            print "filter_wpts"
            print len(filtered_wpts)
            printnames(filtered_wpts)
#           pprint(filtered_wpts, width=132)
            print

    ########################################################################

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
                formatter=optparse.TitledHelpFormatter(),
                usage=globals()['__doc__'],
                version=__VERSION__)
        parser.add_option ('-d', '--debug', action='store_true',
                default=False, help='debug')
        parser.add_option ('-v', '--verbose', action='store_true',
                default=False, help='verbose output')
        (options, args) = parser.parse_args()
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.verbose: print time.asctime()
        exit_code = main(args, options)
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

#######################################################################
# vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
