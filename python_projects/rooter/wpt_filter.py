# coding=utf-8

"""Filter route waypoints to remove 'USER2 == 'SKIP' waypoints.

SYNOPSIS

    wpt_filter [-h] [-v,--verbose] [--version] [-d, --debug] { filename }

DESCRIPTION

    Filter waypoints from a route to remove User2 == "SKIP" values in
    preparation for building a Google Earth route

EXAMPLES

    python wpt_filter # operates on "default.gpx"

    python wpt_filter filename # operates on "filename"

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

"""

from __future__ import print_function
import sys
from pprint import pprint, pformat
from xml.etree import ElementTree as ET

assert sys.version_info > (3, ), "Python 3 required"

########################################################################

__VERSION__ = "0.1.2"
__DATE__ = "2017-07-29"

NAMETAG = "{http://www.topografix.com/GPX/1/1}name"  # replaced later

#######################################################################


def apply_wpts_filter(wpts, debug=False):
    """Apply the filter to the wpts list of Elements."""

    extensionstag = wpts[0].tag.replace("wpt", "extensions")
    if debug:
        print("extensionstag: %s" % extensionstag)

    extensions = [w.find(extensionstag) for w in wpts]

    wpt_extension_tag = extensions[0][0].tag
    if debug:
        print("wpt_extension_tag: %s" % wpt_extension_tag)

    wpt_extensions = [e.find(wpt_extension_tag) for e in extensions]
    if debug:
        print("wpt_extensions")
        pprint(wpt_extensions)
        print()

    u2tag = wpt_extensions[0][0].tag.replace("UserFlag", "User2")
    if debug:
        print("u2tag: %s" % u2tag)

    user2 = [w.find(u2tag) for w in wpt_extensions]
    if debug:
        print("user2")
        pprint(user2)
        print()

    filtered_wpts = [
        w for (w, u) in zip(wpts, user2)
        if (u is None) or (u.text != "SKIP")
    ]

    return filtered_wpts

########################################################################


if __name__ == '__main__':

    import argparse
    import textwrap
    import time

    ########################################################################

    def get_wpts(filename, debug=False):
        """Retrieve waypoints from filename."""

        tree = ET.parse(filename)
        root = tree.getroot()

        if debug:
            print("Metadata:")
            metadata = root.find(root.tag.replace("gpx", "metadata"))
            for item in metadata:
                if (item.text is not None) and (item.text.strip()):
                    print("%s: %s" % (item.tag, item.text))
            print()

        # this is needed by printnames in command line test
        global NAMETAG  # pylint: disable=W0603
        NAMETAG = root.tag.replace("gpx", "name")
        print("NAMETAG: %s" % NAMETAG)

        _wpttag = root.tag.replace("gpx", "wpt")
        wpts = root.findall(_wpttag)

        return wpts

    ########################################################################

    def printnames(wpts):
        """Print the names of the waypoints in wpts."""

        for item in wpts:
            name = item.find(NAMETAG).text
            print(name)
        print()

    ########################################################################

    def main(args, options):
        """Main function callable from the console."""

        debug = options.debug
        filename = args[0] if args else "default.gpx"

        if debug:
            print("args:", pformat(args))
            print("options: ", pformat(options))
            print(filename)
            print()

        wpts = get_wpts(filename, debug)

        if debug:
            print("wpts")
            print(len(wpts))
            printnames(wpts)
            print()

        filtered_wpts = apply_wpts_filter(wpts)
        if debug:
            print("filter_wpts")
            print(len(filtered_wpts))
            printnames(filtered_wpts)
            print()

        return 0

    ########################################################################

    try:
        START_TIME = time.time()
        PARSER = argparse.ArgumentParser(
            usage=textwrap.dedent(__doc__),
            )

        PARSER.add_argument(
            '-d',
            '--debug',
            action='store_true',
            default=False,
            help='debug'
            )

        PARSER.add_argument(
            '--version',
            action='version',
            version="Version: %s %s" % (__VERSION__, __DATE__)
            )

        PARSER.add_argument(
            '-v',
            '--verbose', action='store_true',
            default=False,
            help='verbose output'
            )

        PARSER.add_argument(
            "files",
            nargs="*",
            default=["default.gpx"]
        )

        OPTIONS = PARSER.parse_args()
        ARGS = OPTIONS.files

        if OPTIONS.verbose:
            print(time.asctime())

        EXIT_CODE = main(ARGS, OPTIONS)

        if EXIT_CODE is None:
            EXIT_CODE = 0

        if OPTIONS.verbose:
            print(time.asctime())

        if OPTIONS.verbose:
            print('TOTAL TIME IN MINUTES:', end=" ")

        if OPTIONS.verbose:
            print((time.time() - START_TIME) / 60.0)

        sys.exit(EXIT_CODE)

    except KeyboardInterrupt as _error:  # Ctrl-C
        raise _error

    except SystemExit as _error:         # sys.exit()
        raise _error

    # except Exception as _error:
    #     print('ERROR, UNEXPECTED EXCEPTION')
    #     print(str(_error))
    #     traceback.print_exc()
    #     os._exit(1)

#######################################################################
# vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
