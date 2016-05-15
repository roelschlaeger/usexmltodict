# coding=utf-8

"""Perform processing for the Franklin 8x8 Cipher."""

from xml.etree import ElementTree as ET
import string

########################################################################

"""<ONE-LINE-DESCRIPTION>

<DETAILED-DESCRIPTION>"""

__version__ = "$Revision: $".split()[1]
__date__ = "$Date: $".split()[1]

########################################################################


def process_arg(arg, body, options):
    """Process ..."""
    larg = list(arg)
    assert len(larg) == 64

    h1 = ET.SubElement(body, "h3")
    h1.text = arg

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

    for row_number in range(8):
        tr = ET.SubElement(table, "tr")
        for col_number in range(8):
            td = ET.SubElement(tr, "td")
            td.text = larg.pop(0)

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
        paragraph.text = string.uppercase
        paragraph = ET.SubElement(
            body,
            "p",
            style="font-family:BabelStone PigPen;font-size:110%;color:blue"
        )

        paragraph.text = string.lowercase
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

        print ET.tostring(html)

    ########################################################################

    from optparse import OptionParser
    # import sys

    USAGE = "%prog { options }"
    VERSION = "Version: %(version)s, %(date)s" % {
        "version":   __version__,
        "date":   __date__,
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
