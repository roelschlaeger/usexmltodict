#!C:\Python25\python.exe
# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:tw=0:wm=0:et
# Created:       Sun 08 Aug 2010 10:04:57 PM CDT
# Last Modified: Tue 04 Feb 2014 02:51:31 PM CST
# $Id: et.py 193 2011-01-08 04:28:44Z harry $

"""Process a .gpx file to extract pertinent data fields"""

########################################################################

from pprint import pprint, pformat
from xml.etree import ElementTree as ET
import codecs
import glob
import os.path
import re
import StringIO
import sys
import zipfile

########################################################################

GLOBAL_MIN_INDEX = 110

# HTTP_TRAILER = "&pf=y&log=y&decrypt=y"
HTTP_TRAILER = "&lc=10&decrypt=y"

########################################################################


def tag_factory(schema):
    """return a function that generates a tag for a given schema"""

    schema_string = "%s%%s" % schema
    return lambda x: schema_string % x

########################################################################

# generate_gpx_tag values, filled in after the 'gpx' root element is read

# gpx tags
# pylint: disable=E0221
AUTHOR = None
BOUNDS = None
CMT = None
DESC = None
EMAIL = None
KEYWORDS = None
LINK = None
METADATA = None
NAME = None
RTE = None
RTE_CMT = None
RTE_DESC = None
RTE_EXTENSIONS = None
RTE_NAME = None
RTE_SYM = None
RTE_TIME = None
RTE_TYPE = None
RTEPT = None
SYM = None
TIME = None
TYPE = None
URL = None
URLNAME = None
WPT = None

# extension tags
COUNTY = None
# DNF = None
# FIRSTTOFIND = None
# LASTGPXDATE = None
# LOCK = None
SMARTNAME = None
USER2 = None
# USERDATA = None
# USERFLAG = None
# USERSORT = None
# WATCH = None
WPTEXTENSION = None

# cache tags
CACHE = None
CONTAINER = None
DIFFICULTY = None
ENCODED_HINTS = None
GSNAME = None
OWNER = None
PLACED_BY = None
TERRAIN = None

CHILD_SKIP_TAGS = []
GRANDCHILD_SKIP_TAGS = []

########################################################################


def make_cache_tags(schema="{http://www.groundspeak.com/cache/1/0/1}"):

    global CACHE, CONTAINER, DIFFICULTY, ENCODED_HINTS, GSNAME, OWNER
    global PLACED_BY, TERRAIN

    generate_cache_tag = tag_factory(schema)

    CACHE = generate_cache_tag("cache")
    CONTAINER = generate_cache_tag("container")
    DIFFICULTY = generate_cache_tag("difficulty")
    ENCODED_HINTS = generate_cache_tag("encoded_hints")
    GSNAME = generate_cache_tag("name")
    OWNER = generate_cache_tag("owner")
    PLACED_BY = generate_cache_tag("placed_by")
    TERRAIN = generate_cache_tag("terrain")

########################################################################


def make_extension_tags(schema="{http://www.gsak.net/xmlv1/5}"):

    global WPTEXTENSION, USER2, COUNTY, SMARTNAME

    generate_wpt_extension_tag = tag_factory(schema)

    WPTEXTENSION = generate_wpt_extension_tag("wptExtension")
    # USERFLAG = generate_wpt_extension_tag("UserFlag")
    # LOCK = generate_wpt_extension_tag("Lock")
    # DNF = generate_wpt_extension_tag("DNF")
    # WATCH = generate_wpt_extension_tag("Watch")
    # USERDATA = generate_wpt_extension_tag("UserData")
    # FIRSTTOFIND = generate_wpt_extension_tag("FirstToFind")
    USER2 = generate_wpt_extension_tag("User2")
    COUNTY = generate_wpt_extension_tag("County")
    # USERSORT = generate_wpt_extension_tag("UserSort")
    SMARTNAME = generate_wpt_extension_tag("SmartName")
    # LASTGPXDATE = generate_wpt_extension_tag("LastGpxDate")

########################################################################


def make_gpx_tags(root_tag="{http://www.topografix.com/GPX/1/0}"):
    """create schema tags for GPX/1/0"""

    global AUTHOR, BOUNDS, CMT, DESC, EMAIL, KEYWORDS, NAME, SYM, TIME, TYPE
    global URL, URLNAME, WPT, METADATA, LINK, RTE, RTEPT, RTE_TIME, RTE_NAME
    global RTE_CMT, RTE_DESC, RTE_SYM, RTE_TYPE, RTE_EXTENSIONS

    generate_gpx_tag = tag_factory(root_tag)

    AUTHOR = generate_gpx_tag("author")         # not used, just skipped
    BOUNDS = generate_gpx_tag("bounds")         # not used, just skipped
    CMT = generate_gpx_tag("cmt")               # not used, just skipped
    DESC = generate_gpx_tag("desc")             # not used, just skipped
    EMAIL = generate_gpx_tag("email")           # not used, just skipped
    KEYWORDS = generate_gpx_tag("keywords")     # not used, just skipped
    LINK = generate_gpx_tag("link")             # part of GPX/1/1
    METADATA = generate_gpx_tag("metadata")     # part of GPX/1/1
    NAME = generate_gpx_tag("name")
    RTE = generate_gpx_tag("rte")
    RTE_CMT = generate_gpx_tag("cmt")
    RTE_DESC = generate_gpx_tag("desc")
    RTE_EXTENSIONS = generate_gpx_tag("extensions")
    RTE_NAME = generate_gpx_tag("name")
    RTE_SYM = generate_gpx_tag("sym")
    RTE_TIME = generate_gpx_tag("time")
    RTE_TYPE = generate_gpx_tag("type")
    RTEPT = generate_gpx_tag("rtept")
    SYM = generate_gpx_tag("sym")               # not used, just skipped
    TIME = generate_gpx_tag("time")             # not used, just skipped
    TYPE = generate_gpx_tag("type")
    URL = generate_gpx_tag("url")
    URLNAME = generate_gpx_tag("urlname")       # not used, just skipped
    WPT = generate_gpx_tag("wpt")

########################################################################


def make_skip_lists():

    # now use the tags to build the skip lists
    global CHILD_SKIP_TAGS

    CHILD_SKIP_TAGS = [
        AUTHOR,
        BOUNDS,
        DESC,
        EMAIL,
        KEYWORDS,
        LINK,
        METADATA,
        NAME,
        TIME,
        URL,
        URLNAME,
    ]

    global GRANDCHILD_SKIP_TAGS

    GRANDCHILD_SKIP_TAGS = [
        CMT,
        LINK,
        SYM,
        TIME,
        URLNAME,
        WPTEXTENSION
    ]

########################################################################


def find_schema(root, start):

    xsi = "{http://www.w3.org/2001/XMLSchema-instance}"
    for schema in root.attrib[xsi + "schemaLocation"].split()[0::2]:
        if schema.startswith(start):
#           print "{%s}" % schema
            return "{%s}" % schema
    assert 0, "schema for %s not found" % start
    return None

########################################################################


def make_tags(root):
    """Build the global tags for the file being read"""

    make_cache_tags(find_schema(root, "http://www.groundspeak.com/cache"))
    make_extension_tags(find_schema(root, "http://www.gsak.net"))
    make_gpx_tags(find_schema(root, "http://www.topografix.com/GPX"))
    make_skip_lists()

########################################################################


def lat_format(arg):
    """reformat arg into (N|S) dd mm.mmm format
@param arg: latitude
@type arg: string
@returns: string
"""

    arg = float(arg)
    hemisphere = (arg < 0) and "S" or "N"
    arg = abs(arg)
    degrees = int(arg)
    minval = (arg - degrees) * 60.000
    return "%c%02d %2.3f" % (hemisphere, degrees, minval)

########################################################################


def lon_format(arg):
    """reformat arg into (E|W) ddd mm.mmm format
@param arg: longitude
@type arg: string
@returns: string
"""
    arg = float(arg)
    hemisphere = (arg < 0) and "W" or "E"
    arg = abs(arg)
    degrees = int(arg)
    minval = (arg - degrees) * 60.000
    return "%c%03d %2.3f" % (hemisphere, degrees, minval)

########################################################################


def do_output_header():
    """output column headers"""

    cols = [
        "prefix",
        "#",
        "available",
        "archived",
        "description",
        "url",
        "owner",
        "user2",
        "odd",
        "index",
        "name",
        "link",
        "type",
        "container",
        "encoded_hints",
        "latitude",
        "longitude",
        "note",
        "log",
        "smartname",
    ]

    return "\t".join(cols)

########################################################################


def make_row(index, tags):
    """output the collected column data as a tab-delimited row string"""

    # create an empty list to hold output for a line
    out = []

    cache_dict = tags["cache"]

    # assemble column information
    archived = cache_dict["archived"]
    available = cache_dict["available"]
    container = cache_dict["container"] or "ERROR"
    encoded_hints = " ".join((cache_dict["encoded_hints"] or "").split())
    owner = cache_dict["owner"] or ""
#   placed_by     = cache_dict[ "placed_by" ] or ""

    desc = tags["desc"]
    lat = tags["lat"]
    lon = tags["lon"]
    name = tags["name"]

    # split the GC number into prefix and id
    gc_prefix, gc_number = name[:2], name[2:]

    gtype = tags["type"].replace(
        "Geocache|", ""
    ).replace(
        "Cache", ""
    ).replace(
        "Waypoint|", ""
    )

    # get the url, with modifications
    url = tags["url"] or ""
    if url:
        url = url.replace("cache_details.aspx", "cdpf.aspx")
        url += HTTP_TRAILER

#   urlname = tags[ "urlname" ]           # not used

#   try:
#       county = tags[ "wptExtension" ][ "County" ]
#   except KeyError:
#       county = "UNK"

    user2 = tags["wptExtension"].get("User2", "")
    smartname = tags["wptExtension"]["SmartName"]

    # compute odd or even row for background coloring
    odd = ((index - GLOBAL_MIN_INDEX) % 20 == 0 and "even") or "odd"

#   link = "N/A"
    row_number = ((index - GLOBAL_MIN_INDEX) / 10) + 4
    link = "=HYPERLINK(F%d;E%d)" % (row_number, row_number)

    log = '=CONCATENATE($a$1;" ";R%d;" Thanks, ";G%d;", for placing this cache! -- roelsch, St. Charles, MO.")' % (row_number, row_number)

    # cleanup non GC items
    if gc_prefix != "GC":
        gc_number = "None"
        available = "N/A"
        archived = "N/A"
        gtype = ""
        link = "=E%d" % row_number
        container = ""
        encoded_hints = ""
        owner = ""
        url = ""                    # output the column information to the list
        log = ""                    # no log if not a waypoint

    out.append(gc_prefix)               # A: GC
    out.append(gc_number)               # B: GC#
    out.append(available)               # C: True | False
    out.append(archived)                # D: True | False
    out.append(desc)                    # E: A Tiny Park by RGS (2.5/1)
    out.append(url)                     # F: http://www.geocaching.com/seek...
    out.append(owner)                   # G: RGS
    out.append(user2)                   # H: USER2
    out.append(odd)                     # I: odd/even
    out.append(str(index))              # J: 110
    out.append(name)                    # K: GC17KCY
    out.append(link)                    # L: =HYPERLINK(F2,E2)
    out.append(gtype)                   # M: Traditional
    out.append(container)               # N: Micro
    out.append(encoded_hints)           # O: Sit a spell.
    out.append(lat_format(lat))         # P: 38.576333
    out.append(lon_format(lon))         # Q: -90.355583
    out.append("")                      # R: note
    out.append(log)                     # S: log
    out.append(smartname)               # T: smartname

    # for a tab-delimited output string
#   out = map( str, out )
    output_string = "\t".join(map(str, out))

    # and fixup any unicode errors
    return output_string.encode('utf-8', 'ignore')

########################################################################


def getzipfile(arg):
    """return the data contained in the L{arg} zipfile"""

    z_file = zipfile.ZipFile(arg, "r")
    namelist = z_file.namelist()
    if len(namelist) != 1:
        z_file.printdir()
        raise ValueError, "Expecting a zip file with a single payload"

    return StringIO.StringIO(z_file.read(namelist[0]))

########################################################################


def create_tags_dictionary(child):
    """create a tags dictionary for a child node; all output fields will be
derived from this data structure"""

    # create a dictionary of keywords and empty strings
    tags = {}.fromkeys(
        [
            "cache",
            "desc",
            "lat",
            "lon",
            "name",
            "url",
            #   "urlname",              # not used
            "wptExtension",
        ],
        ''
    )

    # fill in lat and lon from the child
    tags.update(child.attrib)

    # set up cache subdictionary
    tags["cache"] = {}.fromkeys(
        [
            "archived",
            "available",
            "container",
            # "difficulty",
            "encoded_hints",
            # "id",
            "name",
            "owner",
            "placed_by",
            # "terrain",
        ],
        'N/A'
    )

    # set up wptExtension subdictionary
    tags["wptExtension"] = {}.fromkeys(
        [
            #   "UserFlag",
            #   "Lock",
            #   "DNF",
            #   "Watch",
            #   "UserData",
            #   "FirstToFind",
            #   "UserSort",
            "SmartName",
            "User2",
            "County",
            #   "LastGpxDate",
        ],
        'UNK'
    )

    return tags

########################################################################


def striptag(tag):
    """split a tag into schema and tag parts, returning the tag"""

    re_match = re.match("(\{.*\})(.*)", tag)
    if re_match:
        _schema, tag = re_match.groups()
    else:
        raise ValueError, "tag not found in %s" % tag
    return tag

########################################################################


def handle_wptextension(grandchild, tags):

    c3tags = {}
    for child3 in grandchild.getchildren():
        if child3.tag in [COUNTY, SMARTNAME, USER2]:
            if child3.text:
                c3tags[striptag(child3.tag)] = child3.text.rstrip()

    tags["wptExtension"] = c3tags

########################################################################

OPTIONS_DEBUG = False

########################################################################


def handle_cache(grandchild, tags):

    # capture the cache attributes
    if OPTIONS_DEBUG:
        pprint(grandchild.attrib)

    # collection place for the child tags
    c3tags = {}.fromkeys(
        [
            "archived",
            "available",
            "container",
            # "difficulty",
            "encoded_hints",
            # "id",
            "name",
            "owner",
            "placed_by",
            # "terrain",
        ], ''
    )

    # update the 'archived', 'available', and 'id' tags
    c3tags.update(grandchild.attrib)

    # look at each of the grandchildren
    for child3 in grandchild.getchildren():

        if child3.tag in [
            CACHE,
            CONTAINER,
            DIFFICULTY,
            TERRAIN,
            ENCODED_HINTS,
            OWNER,
            PLACED_BY,
            GSNAME
        ]:
            c3tags[striptag(child3.tag)] = child3.text

    tags["cache"] = c3tags

########################################################################


def process_11_extensions(node, tags):
    """Handle the <extensions> tag introduced in GPX/1/1"""

    for child in node:

        if child.tag == WPTEXTENSION:
            handle_wptextension(child, tags)
        elif child.tag == CACHE:
            handle_cache(child, tags)
        else:
            print "process_11_extensions unhandled: %s" % child.tag

########################################################################


def process_wpt(child, grandchild_skip_tags):
    """collect waypoint data items into a dictionary"""

    # set up the tags data structure
    tags = create_tags_dictionary(child)

    # look at the wpt's children
    for grandchild in child.getchildren():

        # look inside the RTE_EXTENSIONS tag
        if grandchild.tag == RTE_EXTENSIONS:
            process_11_extensions(grandchild, tags)

        # look inside the CACHE tag
        elif grandchild.tag == CACHE:
            handle_cache(grandchild, tags)

        # look inside the WPTEXTENSION tag
        elif grandchild.tag == WPTEXTENSION:
            handle_wptextension(grandchild, tags)

        # grab the text for these tags
        elif grandchild.tag in [DESC, NAME, TYPE, URL]:
            tags[striptag(grandchild.tag)] = grandchild.text

        # handle another curve from GPX/1/1
        elif grandchild.tag in [LINK]:
            tags["url"] = grandchild.attrib["href"]

#       elif grandchild.tag in [ LINK ]:
#           tags[ "url" ] = grandchild.attrib[ "href" ]
#           tags[ "urlname" ] = grandchild.find( "text") or ""

        # skip these tags
        elif grandchild.tag in grandchild_skip_tags:
            pass

        else:
            print >> sys.stderr, \
                "UNEXPECTED GRANDCHILD TAG: '%s' '%s' '%s'" % (
                    grandchild.tag,
                    grandchild.text,
                    grandchild.attrib
                )
            grandchild_skip_tags.append(grandchild.tag)

    return tags

########################################################################


def process_tree(index, tree):
    """parse the tree generating .xls text output"""

    # a list to hold the output lines
    outlines = ["Geocaching with Mean Gene and The Rooter", ""]

    # output the header
    outlines.append(do_output_header())

    # get the root of the three
    root = tree.getroot()

    # create tags
    make_tags(root)

    child_skip_tags = CHILD_SKIP_TAGS
    grandchild_skip_tags = GRANDCHILD_SKIP_TAGS

    # look at the children
    for child in root.getchildren():

        # look at each waypoint
        if child.tag == WPT:

            tags = process_wpt(child, grandchild_skip_tags)
            outlines.append(make_row(index, tags))
            index += 10

        elif child.tag == RTE:
            process_rte(child)

        # skip these tags
        elif child.tag in child_skip_tags:
            pass

        else:
            print >> sys.stderr,     \
                "UNEXPECTED CHILD TAG:", \
                child.tag,               \
                child.text,              \
                child.attrib

            child_skip_tags.append(child.tag)

    return "\n".join(outlines)

########################################################################


def make_html_row(index, tags):
    """output the collected column data as an HTML row string"""

    cache_dict = tags["cache"]
    archived = cache_dict["archived"]
    available = cache_dict["available"]
    unavailable = (archived != "False") or (available != "True")

    st_index = str(index)

    desc = tags["desc"]
    name = tags["name"]
    gc_prefix = name[:2]

    url = tags["url"] or ""
    if url:
        url = url.replace("cache_details.aspx", "cdpf.aspx")
        url += HTTP_TRAILER

    if gc_prefix == "GC":
        anchor = "<a target='_blank' href=%s>%s</a><br/>" % (url, desc)
        gname = "<b><font color='red'>%s</font></b>" % name
    else:
        anchor = "%s<br/>" % desc
        gname = name

    if unavailable:
        anchor = "<s>%s</s>" % anchor
        gname = "<s>%s</s>" % gname
        st_index = "<s><b><font color='red'>%s</font></b></s>" % st_index

    out = "   <tr align='center'><td>%s</td><td>%s</td><td>%s</td></tr>" % (
        st_index, gname, anchor
    )

    # fixup any unicode errors
    return out.encode('utf-8', 'ignore')

########################################################################


def html_tree(index, tree):
    """parse the tree generating HTML output of index, name and link"""

    # lists to hold the output lines
    htmllines = []
    bodylines = []

    # pylint: disable-msg=C0301
    htmllines.append('<html>')
    htmllines.append(' <body>')
    htmllines.append('<script type="text/javascript" src="http://code.jquery.com/jquery-1.4.2.js"></script>')
    htmllines.append('<script type="text/javascript" src="js_tempb.js"></script>')

    bodylines.append("  <table id='waypoints' align='center' border='1'>")
    bodylines.append("   <tr><th>Index</th><th>Waypoint</th><th>URL</th></tr>")
    # pylint: enable-msg=C0301

    # get the root of the tree
    root = tree.getroot()
    # create tags and skip lists
    make_tags(root)

    child_skip_tags = CHILD_SKIP_TAGS
    grandchild_skip_tags = GRANDCHILD_SKIP_TAGS

### # now use the tags to build the skip lists
### child_skip_tags = [
###         AUTHOR,
###         DESC,
###         EMAIL,
###         KEYWORDS,
###         BOUNDS,
###         NAME,
###         TIME,
###         URL,
###         URLNAME,
###         METADATA,
###         LINK,
###         ]
### grandchild_skip_tags = [ SYM, TIME, URLNAME, CMT, WPTEXTENSION, LINK ]

    # look at the children
    for child in root.getchildren():

        # look at each waypoint
        if child.tag == WPT:

            tags = process_wpt(child, grandchild_skip_tags)
            bodylines.append(make_html_row(index, tags))
            index += 10

        elif child.tag in [DESC, TIME]:
            tag = striptag(child.tag)
            value = child.text
            htmllines.append(
                "<h3><center>%s: %s</center></h3>" %
                (tag, value)
            )

        # just skip these tags
        elif child.tag in child_skip_tags:
            pass

        else:
            print >> sys.stderr,            \
                "UNEXPECTED CHILD TAG:",    \
                child.tag,                  \
                child.text,                 \
                child.attrib,               \
                "\n",                       \
                pformat(child_skip_tags)

            child_skip_tags.append(child.tag)

    bodylines.append("  </table>")

    htmllines.append("<hr>")
    htmllines += bodylines
    htmllines.append(" </body>")
    htmllines.append("</html>")

    return "\n".join(htmllines)

########################################################################


def do_body(arg, index, options):
    """process file L{filedata}"""

    global GLOBAL_MIN_INDEX
    GLOBAL_MIN_INDEX = index

    filedata = arg

    # if filedata is a .zip file, replace it with the unzipped contents
    if zipfile.is_zipfile(filedata):
        filedata = getzipfile(filedata)

    # convert to ascii
    filedata = StringIO.StringIO(
        codecs.open(
            filedata,
            "r",
            encoding="ascii",
            errors="ignore"
        ).read().decode(
            "utf-8",
            "ignore"
        )
    )

    # parse the input file
    tree = ET.parse(filedata)

    # optionally create HTML output
    if options.html:

        # create a filename with .html extension
        ofile = os.path.splitext(arg)[0] + ".html"

        # create HTML output and write the file
        _tempfile = open(ofile, "w")
        print >> _tempfile, html_tree(index, tree)
        _tempfile.close()
        print >> sys.stderr, "HTML output is in %s" % ofile

    return process_tree(index, tree)

########################################################################


def process_node(node, depth=1, follow=None):
    """Recursively process a waypoint or route node"""

    if follow is None:
        follow = {}

    unseen = []
    for child in node.getchildren():

        if child.tag in follow:
            print "  " * depth, child.tag, child.text, child.attrib
            if type(follow) == type({}):
                aux = follow[child.tag]
            else:
                aux = []
            process_node(child, depth + 1, aux)

        elif not child.tag in unseen:
            print "  " * depth, child.tag, child.text, child.attrib, "UNKNOWN"
            unseen.append(child.tag)

########################################################################


def process_rte(rte):
    """Process an embedded route"""

    process_node(rte, 1,
                 {
                     RTEPT: [
                         RTE_TIME,
                         RTE_NAME,
                         RTE_CMT,
                         RTE_DESC,
                         RTE_SYM,
                         RTE_TYPE,
                         RTE_EXTENSIONS
                     ],
                 }
                 )

########################################################################


def main(args, options):
    """process a .gpx file, generating a .xls output suitable for input to
Excel or Open Office base"""

    # one cache reference counter
#   global index
    index = 110

    # allow globbing
    filelist = []
    for arg in args:
        filelist.extend(glob.glob(arg))

    for arg in filelist:
        print >> sys.stderr, "Processing %s" % arg
        print do_body(arg, index, options)

########################################################################

if __name__ == "__main__":

#   import sys
    from optparse import OptionParser

    USAGE = """%prog - { options } filename { filename ... }

Process one or more .gpx files, formatting the output to stdout as
tab-delimited text suitable for import into a spreadsheet program; stdout may
be redirected to a file using the '>' operator.

If no filename arguments are present, the user is prompted to locate an input
.gpx file and, if that succeeds, the user is prompted to enter an output .xls
file name.
"""

    VERSION = "%prog: Version 1.0.0, Fri 06/13/2008"
    PARSER = OptionParser(usage=USAGE, version=VERSION)

    PARSER.add_option(
        "-d",
        "--debug",
        dest="debug",
        action="store_true",
        help="set debug flag"
    )

    PARSER.add_option(
        "",
        "--html",
        dest="html",
        action="store_false",
        default=True,
        help="do not generate HTML output"
    )

    (OPTIONS, ARGS) = PARSER.parse_args()
    OPTIONS_DEBUG = OPTIONS.debug

    if not ARGS:

        import EasyDialogs

        INPUT_FILENAME = EasyDialogs.AskFileForOpen(
            "Select a .gpx file",
            [
                ("Geographic files (*.gpx)", '*.gpx'),
                ("All files (*.*)",          '*.*'),
            ],
            defaultLocation="*.gpx",
            windowTitle="Open a .gpx file for processing",
        )

        if INPUT_FILENAME:

            ARGS = [INPUT_FILENAME]

            if 0:
                OUTPUT_FILENAME = EasyDialogs.AskFileForSave(
                    "Select an output file; Cancel for stdout",
                    savedFileName="%s.xls" % INPUT_FILENAME
                )
            else:
                OUTPUT_FILENAME = "%s.xls" % INPUT_FILENAME

            print "Writing to OUTPUT_FILENAME=%s" % OUTPUT_FILENAME

            if OUTPUT_FILENAME:
                OUTFILE = open(OUTPUT_FILENAME, "w")
                sys.stdout = OUTFILE
        else:

            PARSER.print_usage()
            sys.exit(2)

    main(ARGS, OPTIONS)

########################################################################
