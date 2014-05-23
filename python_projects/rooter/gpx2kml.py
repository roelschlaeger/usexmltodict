#!/usr/bin/python
# vim:ts=4:sw=4:tw=0:wm=0:et
# $Id: gpx2kml.py 179 2010-09-08 05:07:18Z harry $
# Created: 	     Tue 04 Jun 2009 10:56:11 PM CDT
# Last modified: Fri 23 May 2014 12:07:13 PM CDT

########################################################################

"""Convert an ordered GSAK .gpx waypoint file to a Google Earth .kml file with
waypoints and route path folders."""

__version__ = "$Revision: 179 $".split()[1]
__date__ = "$Date: 2014-05-23 12:04:56 -0500 (Fri, 23 May 2014) $".split()[1]

########################################################################

from xml.etree.ElementTree import Element, ElementTree, SubElement, tostring

import glob
import sys

########################################################################

#: xml namespace for kml 2.2
KML_NS = "http://www.opengis.net/kml/2.2"

########################################################################

# GPXSTYLE_TAG      = '{http://www.topografix.com/GPX/gpx_style/0/2}'
# LABEL_TAG         = '{http://www.topografix.com/GPX/gpx_overlay/0/3}'
# MODIFIED_TIME_TAG = '{http://www.topografix.com/GPX/gpx_modified/0/1}'

########################################################################

CACHE_TAG = '{http://www.groundspeak.com/cache/1/0/1}'
DESC_TAG = None
EXTENSIONS_TAG = None
GPX_TAG = None
NAME_TAG = None
RTE_TAG = None
RTEPT_TAG = None
SYM_TAG = None
TIME_TAG = None
TYPE_TAG = None
URL_TAG = None
URLNAME_TAG = None
WPT_TAG = None

########################################################################

#: cache icons indexed by groundspeak:type
GEOCACHE_ICON_MAPPING = {
    # pylint: disable-msg=C0301
    "Other": "http://maps.google.com/mapfiles/kml/shapes/parking_lot.png",      # [P]
    "Traditional Cache": "http://www.geocaching.com/images/kml/2.png",          # Green cache
    "Multi-cache": "http://www.geocaching.com/images/kml/3.png",                # Event cache
    "Virtual Cache": "http://www.geocaching.com/images/kml/4.png",              # Virtual cache
    "Letterbox Hybrid": "http://www.geocaching.com/images/kml/5.png",           # Letterbox
    "Event Cache": "http://www.geocaching.com/images/kml/6.png",                # Event cache
    "Unknown Cache": "http://www.geocaching.com/images/kml/8.png",              # Unknown cache
    "Webcam Cache": "http://www.geocaching.com/images/kml/11.png",              # Webcam cache
    "Cache In Trash Out Event": "http://www.geocaching.com/images/kml/13.png",  # CITO Event
    "Earthcache": "http://www.geocaching.com/images/kml/earthcache.png",        # Earthcache
    "Wherigo Cache": "http://www.geocaching.com/images/kml/8.png",              # Unknown cache
    # pylint: enable-msg=C0301
}

########################################################################

#: waypoint icons indexed by type
WAYPOINT_ICON_MAPPING = {
    # pylint: disable-msg=E501
    "Waypoint|Parking Area": "http://maps.google.com/mapfiles/kml/shapes/parking_lot.png",        # [P]
    "Waypoint|Question to Answer": "http://maps.google.com/mapfiles/kml/shapes/info_circle.png",  # [?]
    "Waypoint|Stages of a Multicache": "http://maps.google.com/mapfiles/kml/shapes/flag.png",     # [Flag]
    # pylint: enable-msg=E501
}

#: default icon for generic placemarks
DEFAULT_ICON = "http://maps.google.com/mapfiles/kml/pushpin/blue-pushpin.png"

########################################################################

#: tag for a local geocache balloon styleUrl
GEOCACHE_BALLOON_STYLE = "geocache_balloon"

#: tag for a local child waypoint balloon styleUrl
CHILD_WAYPOINT_BALLOON_STYLE = "child_waypoint_balloon"

########################################################################


def pretty_print(ofile, element, indent="\t"):
    """write element to the L{ofile} file with indenting"""

    from xml.dom.minidom import parseString

    txt = tostring(element)
    ofile.write(
        parseString(txt).toprettyxml(
            indent=indent
        ).encode('ascii', 'ignore')
    )

########################################################################


def process_path(path):
    """read in the xml file returning and ElementTree"""

    print "processing file %s" % path

    # read in the gpx/xml file
    return ElementTree(None, path)

########################################################################


def make_folder(name, open_value):
    """create and return a Folder element with the specified name and
open_value"""

    folder = Element("Folder")

    folder_name = SubElement(folder, "name")
    folder_open = SubElement(folder, "open")

    folder_name.text = name
    folder_open.text = open_value

    return folder

########################################################################


def make_placemark(**kwargs):
    """create and return a Placemark element with the specified parameters"""

    placemark = Element("Placemark")

    for _value in kwargs.values():
        placemark.append(_value)

    return placemark

########################################################################


def Data(name, value):
    """create and return a Data element with the specified value"""

    data = Element("Data", {"name": name})
    val = SubElement(data, "value")
    val.text = value
    return data


########################################################################


def make_generic_placemark(wpt):
    """make a placemark without a styleUrl reference"""

    ########################################################################

    def get_gpx_text(tag):
        """return found gpx tag.text or empty string"""
        value = wpt.find(GPX_TAG + tag)
        if value is not None:
            return value.text
        return ""

    ########################################################################

    name = Element("name")
    style = Element("Style")
    xdata = Element("ExtendedData")
    point = Element("Point")

    wpt_name = get_gpx_text("name")
    wpt_desc = get_gpx_text("desc")
    name.text = "%s (%s)" % (wpt_desc, wpt_name)

    iconstyle = SubElement(style, "IconStyle")
    icon = SubElement(iconstyle, "Icon")
    href = SubElement(icon, "href")
    href.text = DEFAULT_ICON

#   for x in [x for x in wpt]:
    for wpt_child in list(wpt):
        if wpt_child.tag == TIME_TAG:
            continue
        tag = wpt_child.tag[wpt_child.tag.find('}') + 1:]
        xdata.append(Data(tag, wpt_child.text))

    for _key, _value in wpt.attrib.items():
        xdata.append(Data(_key, _value))

    coordinates = SubElement(point, "coordinates")
    coordinates.text = "%s,%s" % (wpt.attrib["lon"], wpt.attrib["lat"])

    placemark = make_placemark(
        name=name,
        style=style,
        extendeddata=xdata,
        point=point,
    )

    return placemark

########################################################################


def make_waypoint_placemark(wpt):
    """create and return a Waypoint placemark using the
CHILD_WAYPOINT_BALLOON_STYLE style"""

    ########################################################################

    def get_gpx_text(tag):
        """return found gpx tag.text value or empty string"""
        value = wpt.find(GPX_TAG + tag)
        if value is not None:
            return value.text
        return ""

    ########################################################################

    name = Element("name")
    styleurl = Element("styleUrl")
    style = Element("Style")
    xdata = Element("ExtendedData")
    point = Element("Point")

    wpt_name = get_gpx_text("name")
    wpt_desc = get_gpx_text("desc")
    name.text = "%s (%s)" % (wpt_desc, wpt_name)

    styleurl.text = "#%s" % CHILD_WAYPOINT_BALLOON_STYLE

    iconstyle = SubElement(style, "IconStyle")
    icon = SubElement(iconstyle, "Icon")
    href = SubElement(icon, "href")
    wpt_waypoint_type = get_gpx_text("type")
    href.text = WAYPOINT_ICON_MAPPING.get(
        wpt_waypoint_type,
        "http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png"
    )

#   for x in [x for x in wpt ]:
    for wpt_child in list(wpt):
        if wpt_child.tag == TIME_TAG:
            continue
        tag = wpt_child.tag[wpt_child.tag.find('}') + 1:]
        xdata.append(Data(tag, wpt_child.text))

    coordinates = SubElement(point, "coordinates")
    coordinates.text = "%s,%s" % (wpt.attrib["lon"], wpt.attrib["lat"])

    placemark = make_placemark(
        name=name,
        styleurl=styleurl,
        style=style,
        extendeddata=xdata,
        point=point,
    )

    return placemark

########################################################################


def make_geocache_placemark(wpt):
    """create and return a Waypoint placemark using the
GEOCACHE_BALLOON_STYLE style"""

    # create elements needed for creating a placemark
    name = Element('name')

    styleurl = Element("styleUrl")
    styleurl.text = "#%s" % GEOCACHE_BALLOON_STYLE

    style = Element("Style")
    iconstyle = SubElement(style, "IconStyle")
    icon = SubElement(iconstyle, "Icon")
    href = SubElement(icon, "href")
    href.text = "http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png"

    xdata = Element("ExtendedData")
    xdata.append(Data("gc_num", wpt.find(NAME_TAG).text))

    description = wpt.find(DESC_TAG).text

    wpt_name = wpt.find(NAME_TAG).text
    name_text = "%s (%s)" % (description, wpt_name)
    name.text = name_text.replace("-", " ")

    # my additions
    if wpt.find(URL_TAG) is not None:
        xdata.append(Data("gc_url", wpt.find(URL_TAG).text))
    xdata.append(Data("gc_type", wpt.find(TYPE_TAG).text))

    # the location of the 'cache' tag has changed, now it is part of
    # <extensions>
    cache = None
    if GPX_TAG == '{http://www.topografix.com/GPX/1/0}':
        cache = wpt.find(CACHE_TAG + "cache")
    else:
        extensions = wpt.find(EXTENSIONS_TAG)
        if extensions is not None:
            cache = extensions.find(CACHE_TAG + "cache")

    if cache is not None:
        def get_cache_text(tag):
            """return found cache tag text value or empty string"""
            value = cache.find(CACHE_TAG + tag)
            if value is not None:
                return value.text
            return ""
        wpt_cache_cont_icon = get_cache_text("container")
        wpt_cache_diff = get_cache_text("difficulty")
        wpt_cache_diff_stars = "stars" + wpt_cache_diff.replace(".", "_")
        wpt_cache_hints = get_cache_text("encoded_hints")
        wpt_cache_long_desc = get_cache_text("long_description")
        wpt_cache_placer = get_cache_text("placed_by")
        wpt_cache_placer_id = cache.find(CACHE_TAG + "owner").attrib["id"]
        wpt_cache_short_desc = get_cache_text("short_description")
        wpt_cache_terr = get_cache_text("terrain")
        wpt_cache_terr_stars = "stars" + wpt_cache_terr.replace(".", "_")
        wpt_cache_type = get_cache_text("type")
        wpt_cache_attributes = ", ".join(
            ["%s=%s" % (k, v) for k, v in cache.attrib.items()]
        )

        xdata.append(Data("gc_cont_icon", wpt_cache_cont_icon))
        xdata.append(Data("gc_diff", wpt_cache_diff))
        xdata.append(Data("gc_diff_stars", wpt_cache_diff_stars))
        xdata.append(Data("gc_hints", wpt_cache_hints))
        xdata.append(Data("gc_long_desc", wpt_cache_long_desc))
        xdata.append(Data("gc_name", description))
        xdata.append(Data("gc_placer", wpt_cache_placer))
        xdata.append(Data("gc_placer_id", wpt_cache_placer_id))
        xdata.append(Data("gc_short_desc", wpt_cache_short_desc))
        xdata.append(Data("gc_terr", wpt_cache_terr))
        xdata.append(Data("gc_terr_stars", wpt_cache_terr_stars))
        xdata.append(Data("gc_wpt_cache_type", wpt_cache_type))
        xdata.append(Data("gc_wpt_cache_attr", wpt_cache_attributes))

        href.text = GEOCACHE_ICON_MAPPING.get(
            wpt_cache_type,
            "http://www.geocaching.com/images/kml/1.png"
        )
        xdata.append(Data("gc_icon",       href.text))

        # modify the name to reflect availability and archive status
        archived = cache.attrib["archived"]
        available = cache.attrib["available"]
        if archived == "True":
            name.text = "<font color='red'>%s</font>" % name.text
            xdata.append(
                Data(
                    "gc_issues",
                    "<tt><b>This cache is permanently archived</b></tt>"
                )
            )

        elif available == "False":
            name.text = "<s>%s</s>" % name.text
            xdata.append(
                Data(
                    "gc_issues",
                    "<tt><b>This cache is temporarily unavailable</b></tt>"
                )
            )

        else:
            xdata.append(Data("gc_issues", ""))

    point = Element("Point")
    coordinates = SubElement(point, "coordinates")
    coordinates.text = "%s,%s" % (wpt.attrib["lon"], wpt.attrib["lat"])

    placemark = make_placemark(
        name=name,
        styleurl=styleurl,
        style=style,
        extendeddata=xdata,
        point=point,
    )

    return placemark

########################################################################


def create_wpts_folder(wpts):
    """create a .kml Folder element containing waypoint information

Each waypoint contains the following subelements::

    <Element {http://www.topografix.com/GPX/1/0}time at b63378>,
    <Element {http://www.topografix.com/GPX/1/0}name at b63418>,
    <Element {http://www.topografix.com/GPX/1/0}desc at b633f0>,
    <Element {http://www.topografix.com/GPX/1/0}url at b634b8>,
    <Element {http://www.topografix.com/GPX/1/0}urlname at b63508>,
    <Element {http://www.topografix.com/GPX/1/0}sym at b63558>,
    <Element {http://www.topografix.com/GPX/1/0}type at b635a8>,
    <Element {http://www.gsak.net/xmlv1/3}wptExtension at b63620>,
    <Element {http://www.groundspeak.com/cache/1/0}cache at b635f8>]

The cache element contains::

    <Element {http://www.groundspeak.com/cache/1/0}name at b69030>,
    <Element {http://www.groundspeak.com/cache/1/0}placed_by at b69238>,
    <Element {http://www.groundspeak.com/cache/1/0}owner at b69288>,
    <Element {http://www.groundspeak.com/cache/1/0}type at b692d8>,
    <Element {http://www.groundspeak.com/cache/1/0}container at b69328>,
    <Element {http://www.groundspeak.com/cache/1/0}difficulty at b69378>,
    <Element {http://www.groundspeak.com/cache/1/0}terrain at b693c8>,
    <Element {http://www.groundspeak.com/cache/1/0}country at b69418>,
    <Element {http://www.groundspeak.com/cache/1/0}state at b69468>,
    <Element {http://www.groundspeak.com/cache/1/0}short_description at b69508>,
    <Element {http://www.groundspeak.com/cache/1/0}long_description at b69170>,
    <Element {http://www.groundspeak.com/cache/1/0}encoded_hints at b69558>,
    <Element {http://www.groundspeak.com/cache/1/0}logs at b695a8>,
    <Element {http://www.groundspeak.com/cache/1/0}travelbugs at b695f8>]

"""

    folder = make_folder("Waypoints", "1")

    for wpt in wpts:

        wpt_type = wpt.find(TYPE_TAG)

        if (wpt_type is None):
            placemark = make_generic_placemark(wpt)

        elif (wpt_type.text.startswith("Waypoint|")):
            placemark = make_waypoint_placemark(wpt)

        elif wpt_type.text.startswith("Geocache|"):
            placemark = make_geocache_placemark(wpt)

        else:
            placemark = make_generic_placemark(wpt)

        folder.append(placemark)

    return folder

########################################################################


def create_path_placemark(wpts):
    """create and return a Placemark containing the coordinates of all the
waypoints in wpts"""

    placemark = Element("Placemark")

    placemark_name = SubElement(placemark, "name")
    placemark_styleurl = SubElement(placemark, "styleUrl")
    placemark_linestring = SubElement(placemark, "LineString")

    placemark_name.text = "Path"
    placemark_styleurl.text = "#lineStyle0"

    linestring_tesselate = SubElement(placemark_linestring, "tesselate")
    linestring_coordinates = SubElement(placemark_linestring, "coordinates")

    linestring_tesselate.text = "1"

    coordinates_list = []
    for wpt in wpts:

        lat = wpt.attrib["lat"]
        lon = wpt.attrib["lon"]
        coordinates = "%s,%s" % (lon, lat)
        coordinates_list.append(coordinates)

    linestring_coordinates.text = " ".join(coordinates_list)

    return placemark

########################################################################


def child_waypoint_balloon_style():
    """create and return a Style element suitable for use by a child
waypoint"""

    # define child waypoint balloon style
    style = Element("Style", {"id": CHILD_WAYPOINT_BALLOON_STYLE})
    style_balloon = SubElement(style, "BalloonStyle")
    balloon_text = SubElement(style_balloon, "text")
    balloon_text.text = """
<pre>
<i><b>   name</b></i> = $[name]
<i><b>    cmt</b></i> = $[cmt]
<i><b>   desc</b></i> = $[desc]
<i><b>    url</b></i> = $[url]
<i><b>urlname</b></i> = $[urlname]
<i><b>    sym</b></i> = $[sym]
<i><b>   type</b></i> = $[type]
</pre>
"""

    return style

########################################################################


def geocache_balloon_style():
    """create and return a Style element suitable for use by a geocache"""

    # define geocache balloon style
    style = Element("Style", {"id": GEOCACHE_BALLOON_STYLE})
    balloon = SubElement(style, "BalloonStyle")
    balloon_text = SubElement(balloon, "text")
    balloon_text.text = """
<center>
<a href="http://www.geocaching.com"><img src="http://www.geocaching.com/images/nav/logo_sub.gif"></a>
&nbsp;
<a href="http://www.geocaching.com/seek/cache_details.aspx?wp=$[gc_num]"><b>$[gc_num]</b></a>
&nbsp;
<b>$[gc_name]</b>
<br />
<img src="$[gc_icon]">&nbsp;A <b>$[gc_type]</b>, by <b>$[gc_placer]</b> [<a href="http://www.geocaching.com/profile?id=$[gc_placer_id]">profile</a>]
<br/>
<i><b>Difficulty</b></i>: <img src="http://www.geocaching.com/images/stars/$[gc_diff_stars].gif" alt="$[gc_diff]">&nbsp;($[gc_diff])&nbsp;
<i><b>Terrain</b></i>: <img src="http://www.geocaching.com/images/stars/$[gc_terr_stars].gif" alt="$[gc_terr]">&nbsp;($[gc_terr])&nbsp;
<i><b>Size</b></i>: <img src="http://www.geocaching.com/images/icons/container/$[gc_cont_icon].gif" width="45" height="12">&nbsp;($[gc_cont_icon])
<br />
<i><b>Cache Attributes</b></i>: $[gc_wpt_cache_attr]
<br />
<font size="5" color="red">$[gc_issues]</font>
</center>
<hr>
<i><b>Hint</b></i>: $[gc_hints]
<hr>
<i><b>Short description</b></i>: $[gc_short_desc]
<br />
<hr>
<i><b>Long description</b></i>: $[gc_long_desc]
<br />
"""

    return style

########################################################################


def make_gpx_tags(root):
    """create global GPX_TAG tags"""

    global DESC_TAG, EXTENSIONS_TAG, GPX_TAG, NAME_TAG, RTE_TAG, RTEPT_TAG
    global SYM_TAG, TIME_TAG, TYPE_TAG, URL_TAG, URLNAME_TAG, WPT_TAG

    GPX_TAG = root.tag[:-3]

    DESC_TAG = GPX_TAG + "desc"
    EXTENSIONS_TAG = GPX_TAG + "extensions"
    NAME_TAG = GPX_TAG + "name"
    RTE_TAG = GPX_TAG + 'rte'
    RTEPT_TAG = GPX_TAG + 'rtept'
    SYM_TAG = GPX_TAG + "sym"
    TIME_TAG = GPX_TAG + "time"
    TYPE_TAG = GPX_TAG + "type"
    URL_TAG = GPX_TAG + "url"
    URLNAME_TAG = GPX_TAG + "urlname"
    WPT_TAG = GPX_TAG + 'wpt'

########################################################################


def make_kml(name, input_tree):
    """create and return an ElementTree containing a kml tree reflecting the
contents of the input_tree"""

    # get a list of waypoints to the input document
    root = input_tree.getroot()
    make_gpx_tags(root)

    raw_wpts = [x for x in root if x.tag == WPT_TAG]

    # filter out User2=="SKIP"
    from wpt_filter import apply_wpts_filter
    wpts = apply_wpts_filter(raw_wpts)

    # create a top-level output element
    kml = Element('kml', {"xmlns": KML_NS})
    tree = ElementTree(kml)

    # create a Document
    kml_document = SubElement(kml, 'Document')

    # create name subelement
    kml_document_name = SubElement(kml_document, "name")
    kml_document_name.text = name

    # create open subelement
    kml_document_open = SubElement(kml_document, "open")
    kml_document_open.text = "1"

    # add placemark line style
    kml_document_linestyle0 = SubElement(
        kml_document,
        "Style",
        {"id": "lineStyle0"}
    )
    kml_document_linestyle0_linestyle = SubElement(
        kml_document_linestyle0,
        "LineStyle"
    )
    SubElement(kml_document_linestyle0_linestyle, "color").text = "99ffac59"
    SubElement(kml_document_linestyle0_linestyle, "width").text = "6"

    # add balloon styles
    kml_document.append(geocache_balloon_style())
    kml_document.append(child_waypoint_balloon_style())

    # add waypoint and path folders to Document
    kml_document.append(create_wpts_folder(wpts))
    kml_document.append(create_path_placemark(wpts))

    return tree

########################################################################


def create_kml_file(input_filename, output_filename=None):
    """generate and write a kml output file from the file named
input_filename"""

    if output_filename is None:
        output_filename = input_filename + ".kml"

    input_tree = process_path(input_filename)
    output_tree = make_kml(input_filename, input_tree)

    print "\twriting to %s" % output_filename
    output_file = open(output_filename, "w")
    pretty_print(output_file, output_tree.getroot(), indent=" ")
    output_file.close()

########################################################################


def main(args, options):
    """generate kml file from command line arguments"""

    output_filename = options.output_file

    for arg in args:
        for input_filename in glob.glob(arg):
            create_kml_file(input_filename, output_filename)

########################################################################

if __name__ == "__main__":

    from optparse import OptionParser
#   import sys

    DESCRIPTION = __doc__
    USAGE = "%prog { options } { filename ... } }"
    VERSION = "Version: %s, %s" % (__version__, __date__)
    EPILOG = """If no filename parameter(s) are provided, the user will be
prompted with a file open dialog to select an input .gpx file.  Unless
specified with the -o/--output option, the generated output filename will be
the input filename + ".kml" extension.
"""

    PARSER = OptionParser(
        description=DESCRIPTION,
        usage=USAGE,
        version=VERSION,
        epilog=EPILOG,
    )

    PARSER.add_option("-d",
                      "--debug",
                      dest="debug",
                      action="count",
                      help="increment debug counter"
                      )

    PARSER.add_option("-o",
                      "--output",
                      dest="output_file",
                      action="store",
                      help="set output file (default: %default)",
                      )

    (OPTIONS, ARGS) = PARSER.parse_args()

    if not ARGS:

        import EasyDialogs

        INPUT_FILE = EasyDialogs.AskFileForOpen(
            "Select a .gpx file",
            [
                ("Geographic files (*.gpx)", '*.gpx'),
                ("All files (*.*)",          '*.*'),
            ],
            defaultLocation="*.gpx",
            windowTitle="Open a .gpx file for processing",
        )

        if INPUT_FILE:
            ARGS = [INPUT_FILE]

        else:
            PARSER.print_usage()
            sys.exit(2)

    main(ARGS, OPTIONS)

########################################################################
