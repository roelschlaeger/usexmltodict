# coding=utf-8

"""
make_rtept.py: Create a <rtept> Element for a <gpx> XML file.

Copyright (c) 2016-2017, Robert L. Oelschlaeger,  All Rights Reserved.

Create a ElementTree rtept element suitable for use with Microsoft Streets and
Trips.
"""

########################################################################

from __future__ import print_function
from xml.etree import ElementTree as ET
import os.path
import sys
from gpx2kml import pretty_print

assert sys.version_info > (3, ), "Python 3 required"

########################################################################

__VERSION__ = "0.0.3"  # manual version information
__DATE__ = "2017-07-28"

########################################################################

__CREATOR__ = "make_rtept.py %s" % __VERSION__

GPX_NAMESPACE = "http://www.topografix.com/GPX/1/1"
GSAK_NAMESPACE = "http://www.gsak.net/xmlv1/6"
GROUNDSPEAK_NAMESPACE = "http://www.groundspeak.com/cache/1/0/1"

ITEM_TEXT = "MAKE_RTEPT_WAYPOINT"

ET.register_namespace("", GPX_NAMESPACE)
ET.register_namespace("GSAK", GSAK_NAMESPACE)
ET.register_namespace("groundspeak", GROUNDSPEAK_NAMESPACE)
# ET.register_namespace("xsd", "http://www.w3.org/2001/XMLSchema")
# ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")

########################################################################


def get_usersort(_w0):
    """Get a UserSort value for the current waypoint _w0, if one exists."""
    try:

        value = _w0\
            .find(make_tag("extensions"))\
            .find(make_tag("wptExtension", GSAK_NAMESPACE))\
            .find(make_tag("UserSort", GSAK_NAMESPACE))\
            .text
        # print("Success: %s" % value, list(_w0))
    except AttributeError:
        value = ""

    return value

########################################################################


# pylint: disable=too-many-locals,too-few-public-methods
class DummyText(object):
    """From a text string create an object that has a .text attribute."""

    text = ""

    def __init__(self, item):
        """Create a DummyText object."""
        if item is None:
            self.text = ""
        elif isinstance(item, str):
            self.text = item
        else:
            self.text = item.text

########################################################################


def make_tag(_s, _ns=GPX_NAMESPACE):

    """Create an Element tag from tagname L{_s} and optional namespace
L{_ns}."""

    return "{%s}%s" % (_ns, _s)

########################################################################


ELE_TAG = make_tag("ele")
TIME_TAG = make_tag("time")
MAGVAR_TAG = make_tag("magvar")
GEOIDHEIGHT_TAG = make_tag("geoidheight")
NAME_TAG = make_tag("name")
CMT_TAG = make_tag("cmt")
DESC_TAG = make_tag("desc")
SRC_TAG = make_tag("src")
LINK_TAG = make_tag("link")
SYM_TAG = make_tag("sym")
RTYPE_TAG = make_tag("type")
FIX_TAG = make_tag("fix")
SAT_TAG = make_tag("sat")
HDOP_TAG = make_tag("hdop")
VDOP_TAG = make_tag("vdop")
PDOP_TAG = make_tag("pdop")
AGEOFDGPSDATA_TAG = make_tag("ageofdgpsdata")
DGPSID_TAG = make_tag("dgpsid")
EXTENSIONS_TAG = make_tag("extensions")

USERSORT_TAG = make_tag("UserSort", GSAK_NAMESPACE)

RTEPT_TAG = make_tag("rtept")

WPT_TAG = make_tag("wpt")

########################################################################


def add_rtepts_from_wpts(rte, wpts):
    """Create a series of <rtept> Elements appended to the <rte> Element."""
    # create a list for temporarily storing accumulating rtepts
    rtept_list = []

    # add modified wpts to rte as they are seen
    for wpt in wpts:

        # get location from attributes
        lat = wpt.attrib["lat"]
        lon = wpt.attrib["lon"]

        # make a new <wpt> element from the old one
        new_wpt = ET.Element(WPT_TAG, {"lat": lat, "lon": lon})

        # make an <rtept> element
        rtept = ET.Element(RTEPT_TAG, {"lat": lat, "lon": lon})

        # gather this information first
        _name = DummyText(wpt.find(NAME_TAG))
        _desc = DummyText(wpt.find(DESC_TAG))
        _usersort = DummyText(get_usersort(wpt))

        # pylint: disable=cell-var-from-loop
        def _fabricated_name():
            if _usersort:
                return "%s %s %s " % (_usersort.text, _desc.text, _name.text)
            return "%s %s" % (_desc.text, _name.text)

        # pass along most of the information to the new_wtp (but not
        # extensions)
        for tag in [
                ELE_TAG,                           # KEEP THESE IN THIS ORDER #
                TIME_TAG,                          #
                MAGVAR_TAG,                        #
                GEOIDHEIGHT_TAG,                   #
                NAME_TAG,                          #
                CMT_TAG,                           #
                DESC_TAG,                          #
                SRC_TAG,                           #
                LINK_TAG,                          #
                SYM_TAG,                           #
                RTYPE_TAG,                         #
                FIX_TAG,                           #
                SAT_TAG,                           #
                HDOP_TAG,                          #
                VDOP_TAG,                          #
                PDOP_TAG,                          #
                AGEOFDGPSDATA_TAG,                 #
                DGPSID_TAG,                        # KEEP THESE IN THIS ORDER #
                # EXTENSIONS_TAG                   # not passing extensions
        ]:

            # check for the presence of the tag in the old wpt
            found = wpt.find(tag)

            # if it is there, add it to the <rtept> and new <wpt>, removing the
            # tail information
            if found is not None:

                item2 = ET.SubElement(new_wpt, tag)
                item2.text = found.text

                # interchange the <name> and <desc> tags
                if tag == NAME_TAG:
                    item = ET.SubElement(rtept, tag)
                    # item.text = "%s %s" % (_usersort.text, _desc.text)
                    item.text = _fabricated_name()
                elif tag == DESC_TAG:
                    item = ET.SubElement(rtept, tag)
                    item.text = _name.text
                else:
                    item = ET.SubElement(rtept, tag)
                    item.text = found.text

        rtept_list.append(rtept)
        rte.append(new_wpt)

    # now transfer all of the collected <rtept> data
#   for rtept in rtept_list:
#       rte.append(rtept)
    rte.extend(rtept_list)

#######################################################################


def do_make_rtept(filename, debug=False, outfile=None):
    """Create a route GPX file from pathname."""
    # pylint: disable=global-statement
    global ITEM_TEXT

    from datetime import date
    ITEM_TEXT = str(date.today())

    if outfile is None:
        outfile = filename

        # munge the filename to add .gpx to the end
        head, tail = os.path.split(outfile)
        outname = os.path.join(
            head,
            "%s_est.gpx" % tail.replace(".", "_").replace(" ", "_"))

    if debug:
        print(filename, outname)

    # get wpts elements from an existing file
    root = ET.parse(filename).getroot()
    wpts = root.findall(WPT_TAG)

    # build an output gpx file
    gpx = ET.Element("gpx")
    gpx.attrib["version"] = "1.1"
    gpx.attrib["creator"] = __CREATOR__

    # add all current wpts as-is
    for wpt in wpts:
        for item in wpt.iter():
            item.tail = ""
            txt = item.text
            # print("'%s'" % txt)
            if txt is not None and txt.strip() == "":
                item.text = ""
            if item.tag == RTYPE_TAG:
                item.text = "%s %s" % (ITEM_TEXT, item.text)
        gpx.append(wpt)

    # with a rte
    rte = ET.SubElement(gpx, "rte")

    # add the wpts to the rte as rtepts
    add_rtepts_from_wpts(rte, wpts)

    ofile = open(outname, "w", encoding="utf-8")
    pretty_print(ofile, gpx, indent=" ")
    ofile.close()

    return outname

#######################################################################


if __name__ == "__main__":

    from argparse import ArgumentParser
    import textwrap

    DEFAULT_FILENAME = "topo840b - collinsville IL.gpx"

    #######################################################################

    def process_files(args):
        """Process args.files using make_rtept."""
        if isinstance(args.filename, str):
            args.filename = [args.filename]

        for filename in args.filename:

            output_filename = do_make_rtept(
                filename,
                debug=args.debug,
                outfile=args.outfile
            )

            print(output_filename)

    #######################################################################

    PARSER = ArgumentParser(
        description="Process files using make_rtept().",
        usage=textwrap.dedent(__doc__),
        epilog="Results will be returned in FILENAME.gpx",
    )

    PARSER.add_argument(
        "--version",
        action="version",
        version="%%(prog)s, Version: %s %s" % (__VERSION__, __DATE__)
        )

    PARSER.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Setting the DEBUG flag adds debugging output to the console"
    )

    PARSER.add_argument(
        "filename",
        default=DEFAULT_FILENAME,
        action="store",
        nargs="*",
        help="Specify file(s) to be processed through make_rtept"
    )

    PARSER.add_argument(
        "-o",
        "--outfile",
        action="store",
        help="Specify explicit output filename"
    )

    ARGS = PARSER.parse_args()

    process_files(ARGS)

# end of file
