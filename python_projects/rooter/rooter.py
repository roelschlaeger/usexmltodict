# coding=utf-8

"""
Generate an HTML file from a .gpx route.

SYNOPSIS

    python rooter.py [-h] [-v,--verbose] [--version] [ gpx_filename ]

    where gpx_filename defaults to "default.gpx"

EXAMPLES

    python rooter.py <filename>

EXIT STATUS

AUTHOR

    Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

VERSION

"""

# xpylint: disable=W0603,W0402,R0914,R0915,R0912,W0640
# global
# pylint: disable=W0603
# optparse
# pylint: disable=W0402
# ... defined in loop
# pylint: disable=W0640
# too many branches
# pylint: disable=R0912
# too many local variables
# pylint: disable=R0914
# too many statements
# pylint: disable=R0915

# from __future__ import print_function
from xml.etree import ElementTree as ET
import codecs
import os.path
import sys
from dominate import document
from dominate.tags import table, tr, th, td, br, em, style, a, caption, meta
from degmin import degmin


assert sys.version_info > (3, ), "Python 3 required"

########################################################################

__VERSION__ = "0.0.5"    # rlo
__DATE__ = "2017-07-24"  # rlo

DEBUG = False
ELLIPSIS_MAX = 72

########################################################################


def location_link(lat, lon):
    """Return an anchor tag for (lat, lon) that links to Google Maps."""
    from maplink import maplink
    href = maplink(lat, lon)
    link = "(%s, %s)" % (degmin(lat, "NS"), degmin(lon, "EW"))
    return a(link, cls="latlon", href=href, target="_blank")

########################################################################


def get_wpts(gpxname):
    """Return a waypoint data as a waypoint list and lat/lon dictionary.

    Waypoints are extracted from the 'gpxname' .gpx file. The returned result
    is a list of the waypoints and a dictionary of the waypoint lat/lon
    locations.
    """
    tree = ET.parse(gpxname)
    root = tree.getroot()
    wpts = root.findall(root.tag.replace("gpx", "wpt"))

    latlon_dictionary = {}
    for wpt in wpts:
        lat = wpt.attrib["lat"]
        lon = wpt.attrib["lon"]
        name = wpt.find(wpt.tag.replace("wpt", "name")).text
        latlon_dictionary[name] = (lat, lon)

    return wpts, latlon_dictionary

########################################################################


def ellipsis(_s, _l):
    """
    Return a string of length '_l' at most.

    The returned string results from appending an ellipsis if necessary to
    indicate overflow.
    """
    # TODO this shouldn't happen?
    if _s is None:
        return None

    if len(_s) < _l:
        return _s

    return _s[:_l - 3] + "..."

########################################################################


STYLE = """\
        table { page-break-inside:auto; border-spacing:3px; padding:3px; }
        table, td, th, tr { border:1px solid green; }
        th { background-color: green; color: white; }
        th.tiny { width:3%; }
        th.narrow { width:47%; }
        th.wide { width:50%; }
        tr { page-break-inside:avoid; page-break-after:auto; }
        tr.center { margin-left:auto; margin-right:auto; }
        tr.alt { background-color: #f0f0f0; }
        caption { background-color: #c0c040; \
            font-size: 16px; \
            font-family: "Courier New"; }
        body { font-size: 16px; }
        @media print {
            body { font-size: 8px; font-family: "Courier New" }
            caption { font-size: 10px }
            a { text-decoration: none; font-style: italic; font-weight: bold }
            th { background-color: white; color: black; }
        }
"""


def create_rooter_document(gpxname):
    """Generate the HTML 'Rooter' output document.

    Create a HTML document from the information contained in the .gpx file
    named gpxname.
    """
    print("reading %s" % gpxname)

    wpts, latlon_dictionary = get_wpts(gpxname)

    _w0 = wpts[0]

    def make_wtag(_s):
        """Create a waypoint tag from _s."""
        return _w0.tag.replace("wpt", _s)

    rooter_document = document()

    rooter_document.head = tr(cls="center")
    rooter_document.head.add(th("Geocache", cls="wide"))
    rooter_document.head.add(th("Found By", cls="tiny"))
    rooter_document.head.add(th("Notes", cls="narrow"))

    html_table = table()
    html_table.add(caption("File: %s" % gpxname))
    html_table.add(rooter_document.head)

    # row counter for even/odd formatting
    row_number = 0

    for wpt in wpts:

        w_lat = wpt.attrib["lat"]
        w_lon = wpt.attrib["lon"]
#       w_time = wpt.find(make_wtag("time")).text
        w_name = wpt.find(make_wtag("name")).text
#       _w_cmt = wpt.find(make_wtag("cmt"))
#       w_cmt = _w_cmt is not None and _w_cmt.text
        w_desc = wpt.find(make_wtag("desc")).text
        _w_link = wpt.find(make_wtag("link"))
        w_link_href = _w_link.attrib["href"]
#       w_link_text = _w_link[0].text
#       w_sym = wpt.find(make_wtag("sym")).text
        w_type = wpt.find(make_wtag("type")).text
        w_extensions = wpt.find(make_wtag("extensions"))

        if DEBUG:
            w_format = "%-20s = %-70s"

            print(w_format % ("lat", str(w_lat)))
            print(w_format % ("lon", str(w_lon)))
#           print(w_format % ("time", w_time))
            print(w_format % ("name", w_name))
#           print(w_format % ("cmt", w_cmt))
            print(w_format % ("desc", w_desc))
            print(w_format % ("link_href", w_link_href))
#           print(w_format % ("link_text", w_link_text))
#           print(w_format % ("sym", w_sym))
            print(w_format % ("type", w_type))
            print(w_format % ("extensions", w_extensions))

        _wpt_extension = w_extensions[0]
        _etag = _wpt_extension[0].tag

        def make_etag(_s):
            """Create an etag from _s."""
            return _etag.replace('UserFlag', _s)

        def get_ext(_s):
            """Docstring."""
            tag = make_etag(_s)
            _v = _wpt_extension.find(tag)
            if _v is not None:
                _v = _v.text
            if DEBUG:
                print("%s=%s" % (_s, _v))
            return _v

#       e_userflag = get_ext('UserFlag')
#       e_lock = get_ext('Lock')
#       e_dnf = get_ext('DNF')
#       e_watch = get_ext('Watch')
#       e_userdata = get_ext('UserData')
        e_lat_before_correct = get_ext('LatBeforeCorrect')
        e_lon_before_correct = get_ext('LonBeforeCorrect')
#       e_firsttofind = get_ext('FirstToFind')
        e_user2 = get_ext('User2')
#       e_user3 = get_ext('User3')
#       e_user4 = get_ext('User4')
#       e_county = get_ext('County')
        e_usersort = get_ext('UserSort')
#       e_smartname = get_ext('SmartName')
#       e_lastgpxdate = get_ext('LastGpxDate')
#       e_code = get_ext('Code')
#       e_resolution = get_ext('Resolution')
#       e_ispremium = get_ext('IsPremium')
#       e_favpoints = get_ext('FavPoints')
#       e_gcnote = get_ext('GcNote')
#       e_guid = get_ext('Guid')
#       e_cacheimages = get_ext('CacheImages')
#       e_logimages = get_ext('LogImages')
#       e_customdata = get_ext('CustomData')

####
        def make_ctag(_s):
            """Create a ctag from _s."""
            return ctag.replace('name', _s)

        if len(w_extensions) > 1:
            _wpt_cache = w_extensions[1]

            ctag = _wpt_cache[0].tag

            def get_cext(_s):
                """Docstring."""
                tag = make_ctag(_s)
                _v = _wpt_cache.find(tag)
                if _v is not None:
                    _v = _v.text
                if DEBUG:
                    print("%s=%s" % (_s, _v))
                return _v
        else:

            def get_cext(_s):
                """Docstring."""
                return ""

        c_cache_id = _wpt_cache.attrib["id"]
        c_cache_available = _wpt_cache.attrib["available"]
        c_cache_archived = _wpt_cache.attrib["archived"]
        if DEBUG:
            print(
                c_cache_id,
                c_cache_available,
                c_cache_archived,
                file=sys.stderr
            )

#       c_name = get_cext("name")
#       c_placed_by = get_cext("placed_by")
#       c_owner = get_cext("owner")
#       c_type = get_cext("type")
        c_container = get_cext("container")
#       c_attributes = get_cext("attributes")
#       c_difficulty = get_cext("difficulty")
#       c_terrain = get_cext("terrain")
#       c_country = get_cext("country")
#       c_state = get_cext("state")
#       c_short_description = get_cext("short_description")
#       c_long_description = get_cext("long_description")
        c_encoded_hints = get_cext("encoded_hints")
#       c_logs = _wpt_cache.find(make_ctag("logs"))
#       c_travelbugs = get_cext("travelbugs")

####
        if not w_name.startswith("GC"):
            print("   skipping %s: '%s'" % (w_name, w_desc[:50]))
            continue

        if row_number % 2:
            row = tr(cls="alt")
        else:
            row = tr()
        row_number += 1

        gc_text = td()

        if e_usersort:
            gc_text += "%s: " % e_usersort
        gc_text += a(w_desc, href=w_link_href, target="_blank")
        gc_text += " (%s)" % w_name

        gc_text += br()
        if w_type:
            gc_text += "%s" % w_type.replace("Geocache|", "")
        if c_container:
            gc_text += ", %s" % c_container
#       if log_info:
#           gc_text += br()
#           gc_text += log_info

        # don't publish coordinates for SKIPped geocaches
        if e_user2 is not None and e_user2.startswith("SKIP"):
            # try to locate the puzzle FINAl coordinates
            final_name = w_name.replace("GC", "FL")
            if final_name in latlon_dictionary:
                f_lat, f_lon = latlon_dictionary[final_name]
#               gc_text += " FINAL=(%s, %s)" % (
#                   degmin(f_lat, "NS"),
#                   degmin(f_lon, "EW")
#               )
                gc_text += " FINAL="
                gc_text.add(location_link(f_lat, f_lon))
            else:
                gc_text += " (ignoring published puzzle location)"
        else:
            # gc_text += " (%s, %s)" % (degmin(w_lat, "NS"),
            #                           degmin(w_lon, "EW"))
            gc_text += "  "
            gc_text.add(location_link(w_lat, w_lon))

            if not((e_lat_before_correct is None) and (e_lon_before_correct is
                                                       None)):
                gc_text.add(" (Corrected)")

        if c_encoded_hints:
            gc_text += br()

            gc_em = em("Hint: ")
            for index, hint in enumerate(c_encoded_hints.split("\n")):
                if index:
                    gc_em.add(br())
                gc_em.add(hint)
            gc_text.add(gc_em)

        from latest_log import latest_log
        # get log information from wpt
        log_info = latest_log(wpt)
#       "count": 0,
#       "most_recent_find_date": "",
#       "recent_log_types": [],
#       "most_recent_log": "",
        if log_info["count"]:
            gc_text.add(br())
            gc_text.add("Log count: %d" % log_info["count"])
            gc_text.add(
                " '%s'"
                %
                ellipsis(
                    "".join(
                        x[0] for
                        x in log_info["recent_log_types"]
                    ),
                    ELLIPSIS_MAX
                )
            )
            gc_text.add(br())
            gc_text.add(
                "Most recent log: '%s'"
                %
                ellipsis(log_info["most_recent_log"], ELLIPSIS_MAX)
            )

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
    rooter_document = document(title="Rooter's HTML: %s" % gpxname)

    r_style = style(type="text/css")
    for line in STYLE.split("\n"):
        r_style.add("\n" + line)

    rooter_document.head.add(meta(charset="UTF-8"))
    rooter_document.head.add(r_style)

    r_body = rooter_document.body
    r_body.add(html_table)

    return rooter_document

########################################################################


def make_zipfile(fname):
    """Create a zipfile containing fname."""
    zipdir, zipbase = os.path.split(fname)
    zipfile, _zipext = os.path.splitext(zipbase)
    zipfilename = os.path.join(zipdir, "%s.zip" % zipfile)
    print("%s created" % zipfilename)

    from zipfile import ZipFile
    _zf = ZipFile(zipfilename, "w")
    _arcdir, arcname = os.path.split(fname)
    _zf.write(fname, arcname)
    _zf.close()

########################################################################


def print_rooter_document(gpxname, rooter_document, zipfile=True):
    """Write the document to a utf-8 file.

    Optionally additionally place the result into a .zip compressed file if
    the zipfile flag is True.
    """
    # create the output
    outfiledir, outfilebase = os.path.split(gpxname)

    outfilebase = outfilebase.replace(" ", "_")
    outfilebase = outfilebase.replace(".", "_")

    outfilename = os.path.join(outfiledir, "%s_rooter.html" % outfilebase)

    outfile = codecs.open(
        outfilename,
        "w",
        errors="ignore",
        encoding="utf-8"
    )
    outfile.write(rooter_document.render())
    outfile.close()

    print("%s written" % outfilename)

    if zipfile:
        make_zipfile(outfilename)

########################################################################


def do_rooter(gpxname):
    """Create and print a Rooter file from gpxname .gpx file."""
    _document = create_rooter_document(gpxname)
    print_rooter_document(gpxname, _document)

########################################################################


if __name__ == '__main__':

    # import sys
    # import os
    # import traceback
    import optparse
    import time

    def main():
        """Process command line arguments and options."""
        global OPTIONS, ARGS, DEBUG

        DEBUG = OPTIONS.debug

        do_rooter(ARGS[0])

        return 0

    ########################################################################

    try:
        START_TIME = time.time()
        PARSER = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version='Version: %s %s' % (__VERSION__, __DATE__)
        )
        PARSER.add_option(
            '-d',
            '--debug',
            action='store_true',
            default=False,
            help='debug'
        )
        PARSER.add_option(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )
        (OPTIONS, ARGS) = PARSER.parse_args()
        if len(ARGS) < 1:
            ARGS = ["default.gpx"]
        if OPTIONS.verbose:
            print(time.asctime())

        EXIT_CODE = main()

        if EXIT_CODE is None:
            EXIT_CODE = 0
        if OPTIONS.verbose:
            print(time.asctime())
        if OPTIONS.verbose:
            print('TOTAL TIME IN MINUTES:', end=" ")
        if OPTIONS.verbose:
            print((time.time() - START_TIME) / 60.0)
        sys.exit(EXIT_CODE)
    except KeyboardInterrupt as _exception:      # Ctrl-C
        raise _exception
    except SystemExit as _exception:             # sys.exit()
        raise _exception
    # except Exception as _exception:
    #     print('ERROR, UNEXPECTED EXCEPTION')
    #     print(str(_exception))
    #     traceback.print_exc()
    #     os._exit(1)

# vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
