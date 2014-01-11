#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Fri 10 Jan 2014 11:44:49 AM CST
# Last Modified: Fri 10 Jan 2014 08:36:01 PM CST

"""
SYNOPSIS

    rooter [-h] [-v,--verbose] [--version] [ filename ]

DESCRIPTION

    Generate an HTML cache list file for The Rooter

EXAMPLES

    python rooter.py <filename>

EXIT STATUS

AUTHOR

    TODO: Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

VERSION

    
"""

__VERSION__ = "0.0.1"

DEBUG = False

########################################################################

from dominate.tags import html, head, body, table, tr, th, td, br, em, style, a, caption
from math import trunc
from pprint import pprint, pformat
from xml.etree import ElementTree as ET
import codecs

########################################################################

def get_wpts(gpxname):
    """Return a list of waypoints from 'gpxname' .gpx file"""

    tree = ET.parse(gpxname)
    root = tree.getroot()
    wpts = root.findall(root.tag.replace("gpx", "wpt"))

    return wpts

########################################################################

def degmin(latlon, posneg=" -"):

    v = float(latlon)

    sign = (v < 0)

    v = abs(v)

    degrees, fraction = trunc(v), v - trunc(v)
    minutes = fraction * 60.
    minutes, thousandths = trunc(minutes), trunc((minutes - trunc(minutes))*1000.)

    # apply sign
    if sign:
        s = posneg[1]
    else:
        s = posneg[0]

    s = s.strip()
    s += "%d %d.%03d" % (degrees, minutes, thousandths)

    return s

########################################################################

def create_rooter_html(gpxname):

    wpts = get_wpts(gpxname)

    w0 = wpts[0]
    def make_wtag(s):
        return w0.tag.replace("wpt", s)

    html_table = table(border=1, cellspacing=3, cellpadding=3, align="center")

    r_head = tr(align="center")
    r_head.add(th("Geocache", width="50%"))
    r_head.add(th("Found By", width="10%"))
    r_head.add(th("Notes", width="40%"))

    html_table.add(r_head)
    html_table.add(caption("File: %s" % gpxname))

    row_number = 0

    for wpt in wpts:

        w_lat        = wpt.attrib["lat"]
        w_lon        = wpt.attrib["lon"]
        w_time       = wpt.find(make_wtag("time")).text
        w_name       = wpt.find(make_wtag("name")).text
        _w_cmt       = wpt.find(make_wtag("cmt"))
        w_cmt        = _w_cmt is not None and _w_cmt.text
        w_desc       = wpt.find(make_wtag("desc")).text
        _w_link      = wpt.find(make_wtag("link"))
        w_link_href  = _w_link.attrib["href"]
        w_link_text  = _w_link[0].text
        w_sym        = wpt.find(make_wtag("sym")).text
        w_type       = wpt.find(make_wtag("type")).text
        w_extensions = wpt.find(make_wtag("extensions"))

        if DEBUG:
            w_format = "%-20s = %-70s" 

            print w_format % ("lat",        str(w_lat))
            print w_format % ("lon",        str(w_lon))
            print w_format % ("time",       w_time)
            print w_format % ("name",       w_name)
            print w_format % ("cmt",        w_cmt)
            print w_format % ("desc",       w_desc)
            print w_format % ("link_href",  w_link_href)
            print w_format % ("link_text",  w_link_text)
            print w_format % ("sym",        w_sym)
            print w_format % ("type",       w_type)
            print w_format % ("extensions", w_extensions)

        wptExtension = w_extensions[0]

        etag = wptExtension[0].tag

        def make_etag(s):
            return etag.replace('UserFlag', s)

        def get_ext(s):
            tag = make_etag(s)
            v = wptExtension.find(tag)
            if v is not None:
                v = v.text
            if DEBUG:
                print "%s=%s" % (s, v)
            return v

        e_userflag    = get_ext('UserFlag')
        e_lock        = get_ext('Lock')
        e_dnf         = get_ext('DNF')
        e_watch       = get_ext('Watch')
        e_userdata    = get_ext('UserData')
        e_firsttofind = get_ext('FirstToFind')
        e_user2       = get_ext('User2')
        e_user3       = get_ext('User3')
        e_user4       = get_ext('User4')
        e_county      = get_ext('County')
        e_usersort    = get_ext('UserSort')
        e_smartname   = get_ext('SmartName')
        e_lastgpxdate = get_ext('LastGpxDate')
        e_code        = get_ext('Code')
        e_resolution  = get_ext('Resolution')
        e_ispremium   = get_ext('IsPremium')
        e_favpoints   = get_ext('FavPoints')
        e_gcnote      = get_ext('GcNote')
        e_guid        = get_ext('Guid')
        e_cacheimages = get_ext('CacheImages')
        e_logimages   = get_ext('LogImages')
        e_customdata  = get_ext('CustomData' )

####
        if len(w_extensions) > 1:
            wptCache = w_extensions[1]

            ctag = wptCache[0].tag

            def make_ctag(s):
                return ctag.replace('name', s)

            def get_cext(s):
                tag = make_ctag(s)
                v = wptCache.find(tag)
                if v is not None:
                    v = v.text
                if DEBUG:
                    print "%s=%s" % (s, v)
                return v
        else:

            def get_cext(s):
                return ""

        c_cache_id          = wptCache.attrib["id"]
        c_cache_available   = wptCache.attrib["available"]
        c_cache_archived    = wptCache.attrib["archived"]
        if DEBUG:
            print >> sys.stderr, c_cache_id, c_cache_available, c_cache_archived

        c_name              = get_cext("name")
        c_placed_by         = get_cext("placed_by")
        c_owner             = get_cext("owner")
        c_type              = get_cext("type")
        c_container         = get_cext("container")
        c_attributes        = get_cext("attributes")
        c_difficulty        = get_cext("difficulty")
        c_terrain           = get_cext("terrain")
        c_country           = get_cext("country")
        c_state             = get_cext("state")
        c_short_description = get_cext("short_description")
        c_long_description  = get_cext("long_description")
        c_encoded_hints     = get_cext("encoded_hints")
        c_logs              = get_cext("logs")
        c_travelbugs        = get_cext("travelbugs")

####
        if not w_name.startswith("GC"):
            print "skipping %s" % w_name
            continue

        if row_number % 2:
            row = tr(cls="alt")
        else:
            row = tr()
        row_number += 1

        gc_text = td() 

#       gc_text += "%s %s (%s/%s)" % (w_name, w_desc, c_difficulty, c_terrain)
        if e_usersort:
            gc_text += "%s: " % e_usersort    
        gc_text += a(w_desc, href=w_link_href)
        gc_text += " (%s)" % w_name

        gc_text += br()
        if (w_type):
            gc_text += "%s" % w_type.replace("Geocache|","")
        if (c_container):
            gc_text += ", %s" % c_container
        gc_text += " (%s, %s)" % (degmin(w_lat, "NS"), degmin(w_lon, "EW")) 
        if c_encoded_hints:
            gc_text += br()

            gc_em = em("Hint: ")
            for index, hint in enumerate(c_encoded_hints.split("\n")):
                if index: gc_em.add(br())
                gc_em.add(hint)
            gc_text.add( gc_em )
#           gc_text += em("Hint: %s" % c_encoded_hints

        row.add(gc_text)

        row.add(td())

        gc_text = ""
        if not c_cache_available == "True":
            gc_text += " CACHE NOT AVAILABLE !!"
        if not c_cache_archived == "False":
            gc_text += " CACHE ARCHIVED !!"
        row.add(td(gc_text))

        html_table.add(row)

    # create the rest of the HTML output file
    rooter_html = html(title="Rooter's HTML: %s" % gpxname)

    r_style = style(type="text/css")
#   r_style.add('\nbody { font-family: "Courier New"; }')
    r_style.add('\n    table { page-break-inside:auto }')
    r_style.add('\n    table th tr { border:1px solid green; }')
    r_style.add('\n    th { background-color: green; color: white; }')
    r_style.add('\n    tr { page-break-inside:avoid; page-break-after:auto }')
    r_style.add('\n    tr.alt { background-color: #f0f0f0; }')
    r_style.add('\n    caption { background-color: #c0c040; font-size: 16px; font-family: "Courier New"; }')
    r_style.add('\n')

    r_head = head()
    rooter_html.add(r_head)

    r_head.add(r_style)

    r_body = body()
    rooter_html.add(r_body)

    r_body.add(html_table)

    # create the output
    outfilename = "rooter.html"
    outfile = codecs.open(outfilename, "w", errors="ignore", encoding="utf8")
    outfile.write(unicode(rooter_html))
    outfile.close()

    print "%s written" % outfilename

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

    def main ():

        global options, args

        # TODO: Do something more interesting here...
        print 'Hello world!'

        global DEBUG
        DEBUG = options.debug

        html = create_rooter_html(args[0])

    try:
        start_time = time.time()
        parser = optparse.OptionParser(
                formatter=optparse.TitledHelpFormatter(),
                usage=globals()['__doc__'],
                version='$Id: py.tpl 332 2008-10-21 22:24:52Z root $')
        parser.add_option ('-d', '--debug', action='store_true',
                default=False, help='debug')
        parser.add_option ('-v', '--verbose', action='store_true',
                default=False, help='verbose output')
        (options, args) = parser.parse_args()
        if len(args) < 1:
            args = [ "default.gpx" ]
#           parser.error ('missing argument')
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

