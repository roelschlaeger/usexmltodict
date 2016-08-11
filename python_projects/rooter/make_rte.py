__PROGRAM_NAME__ = "make_rte.py"

from xml.etree import ElementTree as ET
from gpx2kml import pretty_print
from datetime import datetime
from make_rte_wpts import get_wpts
from make_rtept import make_rtept_from_wpts

DEBUG = False
OUTNAME = "_make_rte.xml"
TAG_BASE = "http://www.topografix.com/GPX/1/1/"
ET.register_namespace("", TAG_BASE)

def make_tag(tag, tag_base=TAG_BASE):
    return "{%s}%s" % (tag_base, tag)

class Route(object):
    _last_route = 0

    def __init__(self,
        name,
        cmt="",
        desc="",
        src="",
        link=None,
        number=0,
        rtype="",           # type
        extensions=[],
        rtept=[],
        _debug = DEBUG
        ):
        self._debug = _debug

        self.name = name

        # provide a cmt if none given
        if not cmt:
            cmt = "Generated on %s by '%s'" % (
            datetime.today(),
            __PROGRAM_NAME__
            )
        self.cmt = cmt

        self.desc = desc
        self.src = src
        self.link = link

        # provide a route number if none given
        if number == 0:
            self._last_route += 1
            number = self._last_route
        self.number = number

        self.rtype = rtype              # type
        self.extensions = extensions

        if rtept:
            rtept = make_rtept_from_wpts(rtept)
        self.rtept = rtept

    def to_xml(self):
        rte = ET.Element(make_tag("rte"))

        if self.name or self._debug:
            name = ET.SubElement(rte, make_tag("name"))
            name.text = self.name

        if self.cmt or self._debug:
            cmt = ET.SubElement(rte, make_tag("cmt"))
            cmt.text = self.cmt

        if self.desc or self._debug:
            desc = ET.SubElement(rte, make_tag("desc"))
            desc.text = self.desc

        if self.src or self._debug:
            src = ET.SubElement(rte, make_tag("src"))
            src.text = self.src

        if self.link or self._debug:
            link = ET.SubElement(rte, make_tag("link"))
            link.text = self.link

        if self.number or self._debug:
            number = ET.SubElement(rte, make_tag("number"))
            number.text = str(self.number)

        if self.rtype or self._debug:
            rtype = ET.SubElement(rte, make_tag("type"))
            rtype.text = self.rtype

        if self.extensions or self._debug:
            extensions = ET.SubElement(rte, make_tag("extensions"))
            extensions.text = self.extensions

        if self.rtept or self._debug:
            rtept = ET.SubElement(rte, make_tag("rtept"))
            rtept.text = self.rtept

        return rte

INFILE = "default.gpx"
INFILE = "topo859 - Macon County MO.gpx"
tree = ET.parse(INFILE)
wpts = get_wpts(tree.getroot())
rte = Route(name="My Route", rtept=wpts).to_xml()

outfile = open(OUTNAME, "wb")
pp = pretty_print(outfile, rte, indent="  ")
outfile.close()
print("output is in %s" % OUTNAME)
