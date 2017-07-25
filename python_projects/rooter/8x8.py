# coding=utf-8

"""Perform processing for the Franklin 8x8 Cipher."""

# pylint: disable=invalid-name

from __future__ import print_function

# pylint: disable=multiple-statements
import sys; assert sys.version_info > (3, ), "Python 3 required"  # noqa: E702

from xml.etree import ElementTree as ET
import string
from bs4 import BeautifulSoup


__VERSION__ = "0.0.2"
__DATE__ = "2017-07-25"

OUTFILENAME = "8x8.html"

########################################################################

"""Display information for a Franklin 8x8 Cipher

This program was used to generate the latitude and longitude clues for a
geocache placed along the Centennial Greenway in Saint Charles, MO."""

########################################################################


def process_arg(arg, body, _options):
    """Process ..."""
    larg = list(arg)
    assert len(larg) == 64

    _h1 = ET.SubElement(body, "h3")
    _h1.text = arg

    paragraph = ET.SubElement(
        body,
        "p",
        style="font-family:BabelStone PigPen;font-size:110%;color:green"
    )

    table = ET.SubElement(
        paragraph,
        "table",
        border="1",
        cellspacing="3",
        cellpadding="3"
    )

    for _row_number in range(8):
        _tr = ET.SubElement(table, "tr")
        for _col_number in range(8):
            _td = ET.SubElement(_tr, "td")
            _td.text = larg.pop(0)

########################################################################


if __name__ == "__main__":

    ########################################################################

    def main(args, options):
        """process each of the command line arguments."""
        html = ET.Element("html")
        body = ET.SubElement(html, "body")
        paragraph = ET.SubElement(
            body,
            "p",
            style="font-family:BabelStone PigPen;font-size:110%;color:green"
        )
        paragraph.text = string.ascii_uppercase
        paragraph = ET.SubElement(
            body,
            "p",
            style="font-family:BabelStone PigPen;font-size:110%;color:blue"
        )

        paragraph.text = string.ascii_lowercase
        paragraph = ET.SubElement(
            body,
            "p",
            style="font-family:BabelStone PigPen;font-size:110%;color:red"
            )

        paragraph.text = string.punctuation
        paragraph = ET.SubElement(
            body,
            "p",
            style="font-family:BabelStone PigPen;font-size:110%;color:orange"
        )

        paragraph.text = string.digits

        for arg in args:
            process_arg(arg, body, options)

        html_pretty_print(html)

    ########################################################################

    def html_pretty_print(html):
        """Print the pretty html output to a file."""
        html_result = ET.tostring(html)  # .decode()
        soup = BeautifulSoup(html_result, "lxml")  # make BeautifulSoup
        with open(OUTFILENAME, "w") as outfile:
            print(soup.prettify(), file=outfile)
        print("Output is in %s" % OUTFILENAME)

    ########################################################################

    # pylint: disable=deprecated-module
    from optparse import OptionParser
    # import sys

    USAGE = "%prog { options }"
    VERSION = "Version: %(version)s, %(date)s" % {
        "version":   __VERSION__,
        "date":   __DATE__,
    }

    PARSER = OptionParser(usage=USAGE, version=VERSION)

    PARSER.add_option(
        "-d",
        "--debug",
        dest="debug",
        action="count",
        help="increment debug counter")

    (OPTIONS, ARGS) = PARSER.parse_args()

    if not ARGS:
        ARGS = [
            # 123456789012345678901234567890123456789012345678901234567890123",
            "MXTIRSTHGRXTTNIGIXHEEYEGYTXNIITEUSHTSFGERIETTHIFHXOHEXIETNXGIOPD",
            "TXTGFOERRSXUERIIEXNETPEHDIXSTTTYXXNYEHHETEXXERGINXEEFNHEEWXIMTTS",
        ]

    main(ARGS, OPTIONS)

########################################################################
