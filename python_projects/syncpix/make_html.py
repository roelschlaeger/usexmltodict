#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Sun 05 Jan 2014 05:22:17 PM CST
# Last Modified: Mon 06 Jan 2014 09:02:42 AM CST

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

import datetime
from datetime import tzinfo
from dateutil.tz import tzlocal

results = [ 
    (datetime.datetime(2014, 1, 4, 7, 32, tzinfo=tzlocal()), '0104140732.jpg', (5.946346109026801, 'GC3XMHN', '1030 Bring Me Some Apple Butter!'), (38.36613276, -90.36783504)),
    (datetime.datetime(2014, 1, 4, 7, 44, tzinfo=tzlocal()), '0104140744.jpg', (3.4931177833956992, 'GC3YGHP', "1040 It's Gone To The Dogs!"), (38.36236442, -90.37613522)),
    (datetime.datetime(2014, 1, 4, 7, 56, tzinfo=tzlocal()), '0104140756.jpg', (5.846988627046444, 'GC444NX', '1050 Smelly Cache'), (38.34253854, -90.39008472)),
    (datetime.datetime(2014, 1, 4, 7, 58, tzinfo=tzlocal()), '0104140758.jpg', (6.864276876797739, 'GC444NX', '1050 Smelly Cache'), (38.34255405, -90.39007165)),
    (datetime.datetime(2014, 1, 4, 9, 31, tzinfo=tzlocal()), '0104140931.jpg', (3.9009583519169038, 'GC4QB1R', '1070 South Side Resting Spot'), (37.4902481, -89.67472223)),
    (datetime.datetime(2014, 1, 4, 9, 48, tzinfo=tzlocal()), '0104140948.jpg', (5.114142276256603, 'GC4HKQJ', '1080 Third of August'), (37.39725424, -89.65748979)),
    (datetime.datetime(2014, 1, 4, 9, 55, tzinfo=tzlocal()), '0104140955.jpg', (2.6713757876204696, 'GC47B8E', '1110 Welcome to Brookside Park'), (37.3944919, -89.66412197)),
    (datetime.datetime(2014, 1, 4, 10, 3, tzinfo=tzlocal()), '0104141003.jpg', (3.4705424894899264, 'GC47B92', '1130 Enjoy Your Visit'), (37.39432627, -89.66135426)),
    (datetime.datetime(2014, 1, 4, 10, 7, tzinfo=tzlocal()), '0104141007.jpg', (3.230050242644616, 'GC47HJR', "1140 Salute:  RicknJoy's 5K FTF Gift Cache"), (37.39328851, -89.66282445)),
    (datetime.datetime(2014, 1, 4, 10, 13, tzinfo=tzlocal()), '0104141013.jpg', (3.530892160372228, 'GC47HJY', '1150 All Around Brookside'), (37.39208277, -89.66131537)),
    (datetime.datetime(2014, 1, 4, 10, 26, tzinfo=tzlocal()), '0104141026.jpg', (8.355615143863295, 'GC4HKF0', '1170 First of August'), (37.3928985, -89.66497734)),
#   (datetime.datetime(2014, 1, 4, 10, 34, tzinfo=tzlocal()), '0104141034.jpg', (3.8052384189927566, '001', None), (37.3926892, -89.65830627)),
    (datetime.datetime(2014, 1, 4, 10, 48, tzinfo=tzlocal()), '0104141048.jpg', (5.5992841044042905, 'GC49KDV', '1210 Forked Tree'), (37.38637294, -89.6548862)),
    (datetime.datetime(2014, 1, 4, 10, 57, tzinfo=tzlocal()), '0104141057.jpg', (1.355401013946705, 'GC4HN65', '1230 Fifth of August'), (37.39327191, -89.67494359)),
    (datetime.datetime(2014, 1, 4, 11, 27, tzinfo=tzlocal()), '0104141127.jpg', (3.033548233828268, 'GC4HKP0', '1250 Second of August'), (37.39100997, -89.66888155)),
    (datetime.datetime(2014, 1, 4, 11, 39, tzinfo=tzlocal()), '0104141139.jpg', (3.205076509218175, 'GC4JAME', '1270 Eleventh of August'), (37.3811381, -89.67349738)),
    (datetime.datetime(2014, 1, 4, 11, 48, tzinfo=tzlocal()), '0104141148.jpg', (4.881998386851853, 'GC4JAKD', '1280 Tenth of August'), (37.37960606, -89.67358639)),
    (datetime.datetime(2014, 1, 4, 12, 5, tzinfo=tzlocal()), '0104141205.jpg', (10.853916375509952, 'GC4HQ75', '1300 Seventh of August'), (37.36107149, -89.68532634)),
    (datetime.datetime(2014, 1, 4, 12, 9, tzinfo=tzlocal()), '0104141209.jpg', (5.979341919225754, 'GC4HQ7W', '1310 Ninth of August'), (37.36261787, -89.68496282)),
    (datetime.datetime(2014, 1, 4, 12, 10, tzinfo=tzlocal()), '0104141210.jpg', (5.493055726348085, 'GC4HQ7W', '1310 Ninth of August'), (37.36262315, -89.68496491)),
    (datetime.datetime(2014, 1, 4, 12, 15, tzinfo=tzlocal()), '0104141215.jpg', (3.163803191262003, 'GC4HQ7E', '1320 Eighth of August'), (37.36137592, -89.68328308)),
    (datetime.datetime(2014, 1, 4, 12, 20, tzinfo=tzlocal()), '0104141220.jpg', (2.1454844322044195, 'GC4HQ6Y', '1330 Sixth of August'), (37.3593993, -89.68470398)),
    (datetime.datetime(2014, 1, 4, 12, 53, tzinfo=tzlocal()), '0104141253.jpg', (3.823226974794081, 'GC4HN5A', '1340 Fourth of August'), (37.38530416, -89.65665939)),
    (datetime.datetime(2014, 1, 4, 13, 7, tzinfo=tzlocal()), '0104141307.jpg', (66.54158320018429, 'GC4KQ5E', '1350 Old McKendree Chapel'), (37.3777011, -89.61931667)),
    (datetime.datetime(2014, 1, 4, 13, 9, tzinfo=tzlocal()), '0104141309.jpg', (2.8804672866024483, 'GC4KQ5E', '1350 Old McKendree Chapel'), (37.37817569, -89.61888861)),
    (datetime.datetime(2014, 1, 4, 13, 22, tzinfo=tzlocal()), '0104141322.jpg', (5.9958319313925665, 'GC4KCFN', '1360 Twenty-third of August'), (37.34092198, -89.60137119)),
    (datetime.datetime(2014, 1, 4, 13, 30, tzinfo=tzlocal()), '0104141330.jpg', (5.619435137012092, 'GC4JANH', '1370 Twelfth of August'), (37.34283633, -89.60005372)),
    (datetime.datetime(2014, 1, 4, 13, 35, tzinfo=tzlocal()), '0104141335.jpg', (6.997897562531999, 'GC4JAPW', '1380 Thirteenth of August'), (37.34118643, -89.59882024)),
#   (datetime.datetime(2014, 1, 4, 13, 41, tzinfo=tzlocal()), '0104141341.jpg', (0.195149526742126, '003', None), (37.33896699, -89.59758718)),
#   (datetime.datetime(2014, 1, 4, 13, 51, tzinfo=tzlocal()), '0104141351.jpg', (1.237642677686103, '004', None), (37.33952891, -89.6002833)),
    (datetime.datetime(2014, 1, 4, 14, 5, tzinfo=tzlocal()), '0104141405.jpg', (2.411807067551504, 'GC4JAV6', '1420 Seventeenth of August'), (37.34415472, -89.58989913)),
#   (datetime.datetime(2014, 1, 4, 14, 21, tzinfo=tzlocal()), '0104141421.jpg', (0.8860818679086664, '005', None), (37.34726356, -89.5879883)),
    (datetime.datetime(2014, 1, 4, 14, 28, tzinfo=tzlocal()), '0104141428.jpg', (3.966749414326469, 'GC4JART', '1460 Fifteenth of August'), (37.34670499, -89.59053867)),
#   (datetime.datetime(2014, 1, 4, 14, 35, tzinfo=tzlocal()), '0104141435.jpg', (4.125033266838158, '006', None), (37.34843854, -89.59034789)),
#   (datetime.datetime(2014, 1, 4, 14, 35, tzinfo=tzlocal()), '0104141435a.jpg', (4.125033266838158, '006', None), (37.34843854, -89.59034789)),
    (datetime.datetime(2014, 1, 4, 14, 48, tzinfo=tzlocal()), '0104141448.jpg', (18.483278344499194, 'GC4JV5T', '1490 Eighteenth of August'), (37.34734361, -89.5925401)),
    (datetime.datetime(2014, 1, 4, 14, 51, tzinfo=tzlocal()), '0104141451.jpg', (131.56092604962362, 'GC4KEW1', '1500 Twenty-seventh of August'), (37.34787025, -89.59430767)),
    (datetime.datetime(2014, 1, 4, 14, 59, tzinfo=tzlocal()), '0104141459.jpg', (2.569516260980257, 'GC4KEW1', '1500 Twenty-seventh of August'), (37.34833578, -89.59566604)),
    (datetime.datetime(2014, 1, 4, 14, 59, tzinfo=tzlocal()), '0104141459a.jpg', (2.569516260980257, 'GC4KEW1', '1500 Twenty-seventh of August'), (37.34833578, -89.59566604)),
    (datetime.datetime(2014, 1, 4, 15, 5, tzinfo=tzlocal()), '0104141505.jpg', (4.414519694304989, 'GC4A702', "1520 TheTroublewithTribbles:Tribble157's 1K FTF Gift"), (37.34687774, -89.596291)),
    (datetime.datetime(2014, 1, 4, 15, 11, tzinfo=tzlocal()), '0104141511.jpg', (5.064945708439308, 'GC4JATQ', '1540 Sixteenth of August'), (37.34570688, -89.59376872)),
    (datetime.datetime(2014, 1, 4, 15, 18, tzinfo=tzlocal()), '0104141518.jpg', (1.8568744422439392, 'GC4KEWD', '1560 Twenty-eighth of August'), (37.34203443, -89.59262467)),
    (datetime.datetime(2014, 1, 4, 15, 28, tzinfo=tzlocal()), '0104141528.jpg', (7.271749498355769, 'GC4KCET', '1580 Twenty-first of August'), (37.34071529, -89.59444312)),
    (datetime.datetime(2014, 1, 4, 15, 32, tzinfo=tzlocal()), '0104141532.jpg', (4.091666887520693, 'GC4JV63', '1590 Nineteenth of August'), (37.33863607, -89.59255745)),
    (datetime.datetime(2014, 1, 4, 15, 37, tzinfo=tzlocal()), '0104141537.jpg', (3.7707402549608076, 'GC4KCF9', '1610 Twenty-second of August'), (37.33917343, -89.59032652)),
    (datetime.datetime(2014, 1, 4, 15, 51, tzinfo=tzlocal()), '0104141551.jpg', (14.240352627401478, 'GC3TGA0', '1620 See Southeast #3: Stuck On You - Redoux'), (37.31375766, -89.52889765)),
    (datetime.datetime(2014, 1, 4, 16, 10, tzinfo=tzlocal()), '0104141610.jpg', (2.811583907394454, 'GC4951W', '1670 Missouri "Geocacheology" Degree Challenge'), (37.33381011, -89.54226209))
 ]

import markup
import os.path
from syncpix import PIXDIR

ROUTE_NAME = "topo727 - Cape Girardeau MO"

def main ():

    global options, args


    table = markup.table(border="1", cellspacing="1", cellpadding="1", summary=ROUTE_NAME)

#   caption = markup.caption(ROUTE_NAME)
#   table += caption

    header_row = markup.th("Name") + markup.th("Description") + markup.th( "Link" )
    table += markup.tr(header_row)

#   header = markup.th( header_row )
#   table += header

    for time, filename, gc, tp in results:
#       print time, filename, gc, tp
        d, gcname, gcdesc = gc

        row = markup.tr()
        row += markup.td((str(gcname)), align="center")
        row += markup.td((str(gcdesc)), align="center")
        row += markup.td(markup.a(filename,href=os.path.join(PIXDIR, filename)), align="center")

        table += row

    title = markup.title("Pictures from %s" % ROUTE_NAME)
    head = markup.head(title)
    body = markup.body(table)
    html = markup.html(head + body)

    print html

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
