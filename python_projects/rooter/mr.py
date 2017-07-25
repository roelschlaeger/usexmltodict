# coding=utf-8
"""Process a GSAK .gpx file, converting ordered waypoints into a <rte>."""

# pylint: disable=R0914,R0915,W0603

from __future__ import print_function
import os
import sys
import copy
import lxml.etree as ET

assert sys.version_info > (3, ), "Python 3 required"

########################################################################

__version__ = "0.0.193"  # 20170723 1853 rlo
__date__ = "2017-07-23"  # 20170723 1853 rlo

########################################################################

# global variables

GPX = None
GPX_NAMESPACE = "http://www.topografix.com/GPX/1/1"
LABEL = None
LABEL_NAMESPACE = None

########################################################################


def new_metadata(item, outname):
    """Create a new <metadata> element to relace the one from the GSAK file.

    @param item: the existing metadata item
    @type item:  lxlm.etree.Element
    """

    metadata = ET.Element("metadata")
    metadata.tail = "\n "
    metadata.text = "\n "

    meta_name = ET.Element("name")
    meta_name.tail = "\n  "
    print("*** new_metadata ***", type(outname), outname)
    meta_name.text = os.path.basename(outname)

    desc = ET.Element("desc")
    desc.tail = "\n  "
    desc.text = \
        "Geocache file generated by the Python program 'mr.py' by roelsch"

    author = ET.Element("author")
    author.tail = "\n  "
    author.text = "\n   "

    name = ET.Element("name")
    name.tail = "\n   "
    name.text = "Robert L. Oelschlaeger"

    email = ET.Element("email")
    email.tail = "\n  "
    email.attrib["id"] = "roelschlaeger"
    email.attrib["domain"] = "gmail.com"

    author.append(name)
    author.append(email)

    _copyright = ET.Element("copyright")
    _copyright.tail = "\n  "
    _copyright.text = "\n   "

    year = ET.Element("year")
    year.tail = "\n   "
    year.text = "2010"

    _license = ET.Element("license")
    _license.tail = "\n  "
    _license.text = ""

    _copyright.attrib["author"] = "Robert L. Oelschlaeger"
    _copyright.append(year)
    _copyright.append(_license)

#   link = ET.Element( "link" )
#   link.tail = "\n  "
#   link.text = "\n"

    # get other fields from the old record
    time = item.find(GPX + "time")
    keywords = item.find(GPX + "keywords")
    bounds = item.find(GPX + "bounds")

    # now put the entire <metadata> element together
    metadata.append(meta_name)
    metadata.append(desc)
    metadata.append(author)
    metadata.append(_copyright)
#   metadata.append( link )
    metadata.append(time)
    metadata.append(keywords)
    metadata.append(bounds)

    return metadata

########################################################################


def create_rte_header(route_name, route_label):
    """Create a new <rte> header element from route_name and route_label."""
    # now create the <rte> element
    # <rte>
    #  <name/>
    #  <cmt/>
    #  <desc/>
    #  <link/>
    #  <number/>
    #  <type/>
    #  <extensions>
    #   <label>
    #    <label_text/>
    #   </label>
    #  </extensions>
    #  <rtept/>
    # </rte>

    rte = ET.Element(GPX + "rte")
    rte.tail = "\n"
    rte.text = "\n "

    name = ET.Element(GPX + "name")
    name.tail = "\n "
    name.text = route_name
    rte.append(name)

    cmt = ET.Element(GPX + "cmt")
    cmt.tail = "\n "
    cmt.text = "cmt"
    rte.append(cmt)

    desc = ET.Element(GPX + "desc")
    desc.tail = "\n "
    desc.text = "description"
    rte.append(desc)

    src = ET.Element(GPX + "src")
    src.tail = "\n "
    src.text = "src"
    rte.append(src)

    link = ET.Element(GPX + "link")
    link.tail = "\n "
#   link.text = "link"
    rte.append(link)

    number = ET.Element(GPX + "number")
    number.tail = "\n "
    number.text = "1"
    rte.append(number)

    xtype = ET.Element(GPX + "type")
    xtype.tail = "\n "
    xtype.text = "topo_route"
    rte.append(xtype)

    extensions = ET.Element(GPX + "extensions")
    extensions.text = "\n  "
    extensions.tail = "\n "

    label = ET.Element(LABEL + "label", nsmap={None: LABEL_NAMESPACE})
    label.tail = "\n "
    label.text = "\n  "

    label_text = ET.Element(LABEL + "label_text")
    label_text.tail = "\n  "
    label_text.text = route_label

    label.append(label_text)
    extensions.append(label)

    rte.append(extensions)

    return rte

########################################################################


def create_rtept_from_wpt(wpt):
    """Create a <rtept> element from an existing <wpt> element."""
    # make a copy of the <wpt>
    rtept = copy.deepcopy(wpt)

    # retag it as <rtept>
    rtept.tag = GPX + "rtept"

    # get name and description text
    name = rtept.find(GPX + "name")
    desc = rtept.find(GPX + "desc")

    # get GSAK UserSort information, if available
    usersort_text = ""
    extensions = rtept.find(GPX + "extensions")
    if extensions is not None:
        w0x = extensions[0]  # waypoint extensions
        w0xtag = w0x.tag
        usersort = w0x.find(w0xtag.replace("wptExtension", "UserSort"))
        if usersort is not None:
            usersort_text = "%s - " % usersort.text
        else:
            usersort_text = ""

    name.text = desc.text = "%s%s %s" % (usersort_text, name.text, desc.text)

    # remove some extraneous types the <rtept> doesn't need
    for type_to_remove in ["extensions", "type"]:
        element_to_remove = rtept.find(GPX + type_to_remove)
        if element_to_remove is not None:
            rtept.remove(element_to_remove)

    return rtept

########################################################################


def process_arg(arg, _options):
    """Process command line arguments and options."""
    global GPX
    global GPX_NAMESPACE
    global LABEL
    global LABEL_NAMESPACE

    route_dir, route_file = os.path.split(arg)
    route_name, _route_ext = os.path.splitext(route_file)
    route_label = route_name + "_route"
    outname = os.path.join(route_dir, route_label + ".gpx")

    tree = ET.parse(arg)
    root = tree.getroot()

    # verify we have the right namespace
    root_namespace = root.tag[1:-4]
    if not root_namespace == GPX_NAMESPACE:
        print("Namespace %s mismatch, will try using %s" % (
            GPX_NAMESPACE, root_namespace),
              file=sys.stderr
             )
        GPX_NAMESPACE = root_namespace

    GPX = "{%s}" % GPX_NAMESPACE
    LABEL_NAMESPACE = "http://www.topografix.com/GPX/gpx_overlay/0/3"
    LABEL = "{%s}" % LABEL_NAMESPACE

    tree = ET.parse(arg)
    root = tree.getroot()
    wpts = root.findall(GPX + "wpt")

    _nsmap = {
        None: GPX_NAMESPACE,       # the default namespace (no prefix)
        #           "ol" : LABEL_NAMESPACE,
    }

    gpx = ET.Element(GPX + "gpx", nsmap=_nsmap)  # lxml only!
    gpx.tail = "\n"
    gpx.text = "\n"
    gpx.attrib["creator"] = "'mr.py' by roelsch"
    gpx.attrib["version"] = "%s, %s" % (__version__, __date__)

    # copy the children from the original GSAK file
    for item in root:

        if item.tag == (GPX + "metadata"):
            item = new_metadata(item, outname)

# except for the <desc> tag
#       if item.tag == (GPX + "desc"):
#           item.text = "Geocache route file generated by 'mr.py'"

        # take part of the wpt tags
        if item.tag == (GPX + "wpt"):

            my_name = ""
            if item.find(GPX + "name") is not None:
                my_name = item.find(GPX + "name").text

            my_desc = ""
            if item.find(GPX + "desc") is not None:
                my_desc = item.find(GPX + "desc").text

            # make a copy
            item = copy.deepcopy(item)

            # and remove some things
            for type_to_remove in ["extensions", "type", "name"]:
                element_to_remove = item.find(GPX + type_to_remove)
                if element_to_remove is not None:
                    item.remove(element_to_remove)

            # insert a name replacement from my_desc and my_name
            name_type = ET.Element(GPX + "name")
            name_type.text = "%s %s" % (my_name, my_desc)
            name_type.tail = "\n"
            item.append(name_type)

            # pick a POI type based on my_name[0:2]
            wpt_type = ET.Element(GPX + "type")
            if my_name[0:2] == "GC":
                wpt_type.text = "Geocache"
            else:
                wpt_type.text = "Other"
            wpt_type.tail = "\n"
            item.append(wpt_type)

        gpx.append(item)

    # now create the <rte>
    rte = create_rte_header(route_name, route_label)

    # copying the wpt-s as rtept-s
    for wpt in wpts:
        rtept = create_rtept_from_wpt(wpt)
        rte.append(rtept)

    gpx.append(rte)

    outfile = open(outname, "wb")
#   outfile.write(
#       ET.tostring(
#           gpx,
#           encoding="utf-8",
#           method="xml",
#           pretty_print=True
#       )
#   )
    ofile = ET.ElementTree(gpx)
    print(ofile.__doc__)
    ofile.write(
        outfile,
        encoding="utf-8",
        xml_declaration=True,
        method="xml",
        # short_empty_elements=True
    )
    outfile.close()

    print("output is in %s" % outname)

#


if __name__ == "__main__":

    def main(args, options):
        """Process command line arguments."""
        for arg in args:
            process_arg(arg, options)

    # pylint: disable=deprecated-module
    from optparse import OptionParser

    USAGE = "%prog { options }"
    VERSION = "Version: %(version)s, %(date)s" % {
        "version":   __version__,
        "date":   __date__,
    }

    PARSER = OptionParser(usage=USAGE, version=VERSION)

    PARSER.add_option("-d",
                      "--debug",
                      dest="debug",
                      action="count",
                      help="increment debug counter")

    (OPTIONS, ARGS) = PARSER.parse_args()

    if not ARGS:

        # import EasyDialogs

        from file_dialog_tk import get_gpx_file

        INPUT_FILE = get_gpx_file(
            # title = "Select a .gpx file",
            # initialdir=".",
            filetypes=[
                ("Geographic files (*.gpx)", '*.gpx'),
                ("All files (*.*)", '*.*'),
            ],
            title="Open a .gpx file for processing",
            # defaultLocation="*.gpx",
        )

        # INPUT_FILE = EasyDialogs.AskFileForOpen(
        #     "Select a .gpx file",
        #     [
        #         ("Geographic files (*.gpx)", '*.gpx'),
        #         ("All files (*.*)",          '*.*'),
        #     ],
        #     defaultLocation="*.gpx",
        #     windowTitle="Open a .gpx file for processing",
        # )

        if INPUT_FILE:
            ARGS = [INPUT_FILE]

        else:
            PARSER.print_usage()
            sys.exit(2)

    main(ARGS, OPTIONS)

#
