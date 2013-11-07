#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

"""
SYNOPSIS

    make_route [-h] [-v,--verbose] [--version] filename { filename... }

DESCRIPTION

    Convert the list of waypoints in filename to a route.

EXAMPLES

    make_route "topo720 - Heritage Trail.gpx"

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Name <name@example.org>

LICENSE

    This script is in the public domain.

VERSION

    
"""

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

from xml.etree.ElementTree import parse, dump, Element, ElementTree, register_namespace
from pprint import pprint

########################################################################

RTE_TAG = None
RTEPT_TAG = None
TOPO_SCHEMA = None
WPT_TAG = None
W3_SCHEMA = "http://www.w3.org/2001/XMLSchema-instance"

########################################################################

def make_tag(s, t):
    """Return a search tag from schema s and tag name t"""
    return "{%s}%s" % (s, t)

########################################################################

def make_topo_tag(t):
    return make_tag(TOPO_SCHEMA, t)

########################################################################

def get_topo_schema(root):
    """Return the schema string for topografix"""

    schema_location_tag = make_tag(W3_SCHEMA, "schemaLocation")
    schemas = root.attrib[ schema_location_tag ].split()
    print "\n\t" + "\n\t".join(schemas) + "\n"
    global TOPO_SCHEMA
    TOPO_SCHEMA = schemas[0]
    print "topo_schema = %s" % TOPO_SCHEMA
    return TOPO_SCHEMA

########################################################################

def create_new_route(rte, waypoints):

    for waypoint in waypoints:
        # turn the waypoint into a rtept
        rtept = Element(RTEPT_TAG)
        rtept.attrib = waypoint.attrib
        for item in waypoint:
            if item.tag.find("extension") >= 0:
                continue
            rtept.append(item)
        rte.append(rtept)

    return rte

########################################################################

def process_arg(arg):
    """Process the arg file"""

    print "Processing %s..." % arg
    tree = parse(arg)
    root = tree.getroot()

    global TOPO_SCHEMA
    TOPO_SCHEMA = get_topo_schema(root)

    register_namespace("", TOPO_SCHEMA)

    global WPT_TAG 
    WPT_TAG = make_topo_tag("wpt")
    print "wpt_tag = %s" % WPT_TAG

    global RTEPT_TAG
    RTE_TAG = make_topo_tag("rte")

    global RTEPT_TAG
    RTEPT_TAG = make_topo_tag("rtept")

    waypoints = root.findall(WPT_TAG)

    # create a route from existing waypoints
    rte = Element(RTE_TAG, text="\n", tail="\n")
    rte = create_new_route(rte, waypoints)

    d = {
            "name"        : "Name on GPS",
            "cmt"         : "Comment",
            "desc"        : "Description",
            "src"         : "Source",
            "href"        : "https://drive.google.com/#folders/0ByBZFYeNib-uVG16bk92M3lodU0",
            "r_link_text" : "r_link_text",
            "r_link_type" : "r_link_type",
            "r_link"      : "link"
            }

    r_name = Element(make_topo_tag("name"), text="\n", tail="\n")
    r_name.text = d["name"]
    rte.append(r_name)

    r_cmt = Element(make_topo_tag("cmt"), text="\n", tail="\n")
    r_cmt.text = d["cmt"]
    rte.append(r_cmt)

    r_desc = Element(make_topo_tag("desc"), text="\n", tail="\n")
    r_desc.text = d["desc"]
    rte.append(r_desc)

    r_src = Element(make_topo_tag("src"), text="\n", tail="\n")
    r_src.text = d["src"]
    rte.append(r_src)

    r_link = Element(make_topo_tag("link"), text="\n", tail="\n")
    r_link.attrib["href"] = d["href"]
    r_link_text = Element(make_topo_tag("text"), text="\n", tail="\n")
    r_link_text.text = d["r_link_text"]
    r_link.append(r_link_text)
    r_link_type = Element(make_topo_tag("type"), text="\n", tail="\n")
    r_link_type.text = d["r_link_type"]
    r_link.append(r_link_type)
    r_link.text = d["r_link"]
    rte.append(r_link)

    r_number = Element(make_topo_tag("number"), text="\n", tail="\n")
    r_number.text = "1"
    rte.append(r_number)

    r_type = Element(make_topo_tag("type"), text="\n", tail="\n")
    r_type.text = "Route"
    rte.append(r_type)

    # create a new gpx Element
    gpx = Element(root.tag)

    version = Element(make_topo_tag("version"))
    version.text="1.1"
    gpx.append(version)

    creator = Element(make_topo_tag("creator"))
    creator.text="make_route.py by R. Oelschlaeger"
    gpx.append(creator)

    gpx.append(Element(make_topo_tag("metadata")))
#   gpx.append(Element(make_topo_tag("wpt")))
    gpx.append(rte)
#   gpx.append(Element(make_topo_tag("trk")))

    newtree = ElementTree(gpx)

#   route.write('route.gpx', default_namespace=topo_schema)
    newtree.write('route.gpx', xml_declaration=True)

#   with open("xroute.gpx", "w") as sys.stdout:
    dump(newtree)
    
########################################################################

def main ():

    global options, args

    if len(args) == 0:
        print >> sys.stderr, "Missing argument"
        return False

    for arg in args:
        process_arg(arg)

########################################################################

if __name__ == '__main__':

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
                formatter=optparse.TitledHelpFormatter(),
                usage=globals()['__doc__'],
                version='$Id: py.tpl 332 2008-10-21 22:24:52Z root $')
        parser.add_option ('-v', '--verbose', action='store_true',
                default=False, help='verbose output')
        (options, args) = parser.parse_args()
        if len(args) < 1:
#           parser.error ('missing argument')
            args = [ "topo720 - Heritage Trail.gpx" ]
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
