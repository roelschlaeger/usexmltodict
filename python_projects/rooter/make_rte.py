#!/usr/bin/env python

"""Program to create a .kml route file."""

import sys

from xml.etree import ElementTree as ET
from datetime import datetime
from gpx2kml import pretty_print
from make_rte_wpts import get_wpts
from make_rtept import make_rtept_from_wpts

assert sys.version_info > (3, ), "Python 3 required"

########################################################################

__PROGRAM_NAME__ = "make_rte.py"
__VERSION__ = "0.0.2"
__DATE__ = "2017-07-30"

DEBUG = False
OUTNAME = "_make_rte.xml"
TAG_BASE = "http://www.topografix.com/GPX/1/1/"
ET.register_namespace("", TAG_BASE)

########################################################################


def make_tag(tag, tag_base=TAG_BASE):
    """Return a tag combining L{tag} and L{tag_base}."""
    return "{%s}%s" % (tag_base, tag)


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class Route(object):
    """Define a route."""
    _last_route = 0
    rtept = None  # due to missing function

    # pylint: disable=too-many-arguments
    def __init__(
            self,
            name,
            cmt="",
            desc="",
            src="",
            link=None,
            number=0,
            rtype="",           # type
            extensions=None,
            rtept=None,
            _debug=DEBUG
    ):
        """Class initialization."""

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
        self.extensions = [] if extensions is None else extensions
        try:
            self.rtept = [] if rtept is None else make_rtept_from_wpts(rtept)
        except Warning as _warning:
            print(_warning)
            self.rtept = []

    def to_xml(self):
        """Make an XML rte."""
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


if __name__ == '__main__':

    from argparse import ArgumentParser
    import textwrap

    def main(args, _options):

        """Main function."""

        if args:
            infile = args[0]

            tree = ET.parse(infile)
            wpts = get_wpts(tree.getroot())
            rte = Route(name="My Route", rtept=wpts).to_xml()

            outfile = open(OUTNAME, "w")
            pretty_print(outfile, rte, indent="  ")
            outfile.close()
            print("output is in %s" % OUTNAME)
        else:
            print("'args' is empty", file=sys.stderr)

    PARSER = ArgumentParser(description=textwrap.dedent(__doc__))

    PARSER.add_argument(
        "-v",
        "--version",
        action="version",
        version="%%(prog)s Version: %(__VERSION__)s, %(__DATE__)s" % globals()
    )

    PARSER.add_argument(
        "files",
        nargs="*",
        help="target files",
        default=["topo859 - Macon County MO.gpx"]
    )

    OPTIONS = PARSER.parse_args()

    main(OPTIONS.files, OPTIONS)

# end of file
