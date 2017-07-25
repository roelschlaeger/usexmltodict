#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

"""
SYNOPSIS

    make_gs [-h | --help] [--version] [--verbose] file [ file ... ]

DESCRIPTION

    This file modifies a standard .gpx file for use with GeoSphere by
    prepending the UserSort value to the Code value for a given waypoint.

EXAMPLES

        python make_gs filename.gpx

    results in filename_gs.gpx with the modified contents

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

"""

from __future__ import print_function
from xml.etree import ElementTree as ET

import sys

assert sys.version_info > (3, ), "Python 3 required"

__VERSION__ = "0.0.2"    # updated for Python3
__DATE__ = "2017-07-25"  # updated for Python3

########################################################################


def generate_output_filename(name):
    """Generate an output filename from L{name}."""
    from os.path import split, splitext, join

    # output will be in the current directory
    _dir, outname = split(name)
    root, ext = splitext(outname)

    # append "_gs" to basename
    root += "_gs"

    return join(_dir, root + ext)

########################################################################


GPX_NAMESPACE = "http://www.topografix.com/GPX/1/1"
NSMAP = {
    None: GPX_NAMESPACE,       # the default namespace (no prefix)
}

# GPX = "{%s}" % GPX_NAMESPACE

GSAK_NAMESPACE = "http://www.gsak.net/xmlv1/6"
GROUNDSPEAK_NAMESPACE = "http://www.groundspeak.com/cache/1/0/1"

########################################################################


def register_namespaces():
    """Register XML namespaces in output file."""

    ET.register_namespace(
        "",
        GPX_NAMESPACE
    )
    ET.register_namespace(
        "gsak",
        GSAK_NAMESPACE
    )
    ET.register_namespace(
        "groundspeak",
        GROUNDSPEAK_NAMESPACE
    )

########################################################################


# pylint: disable=too-many-locals
def process_arg(arg):
    """Process a single file."""

    # parse the input
    tree = ET.parse(arg)
    root = tree.getroot()

    def make_tag(tagname):
        """create a new tag based on root.tag"""
        return root.tag.replace("gpx", tagname)

    # generate necessary tags
    wpt_tag = make_tag("wpt")
    name_tag = make_tag("name")
    extensions_tag = make_tag("extensions")
    gsak_tag = "{%s}wptExtension" % GSAK_NAMESPACE

    # get all waypoints
    wpts = root.findall(wpt_tag)

    # change their name elements
    for wpt in wpts:

        # get old ame
        name = wpt.find(name_tag)
        try:
            # name_text = name.text
            name_text = "" if name is None else name.text
        except AttributeError as _error:
            print(_error, file=sys.stderr)
            traceback.print_exc()
            name_text = "None"

        # get UserSort value
        try:
            extensions = wpt.find(extensions_tag)
            gsak = extensions.find(gsak_tag)
            usersort = gsak.find(gsak.tag.replace("wptExtension", "UserSort"))
            usersort_text = "" if usersort is None else usersort.text
        except AttributeError as _error:
            print(_error, file=sys.stderr)
            traceback.print_exc()
            usersort_text = "None"

        # compute a new name
        new_name = "%s %s" % (usersort_text, name_text)
        name.text = str(new_name)

    # create the modified output filename
    outfilename = generate_output_filename(arg)

    # create the binary .gpx file
    with open(outfilename, "wb") as outfile:

        # recreate the tree
        ofile = ET.ElementTree(root)

        # add in the namespaces
        register_namespaces()

        # write the result
        ofile.write(
            outfile,
            encoding="utf-8",
            xml_declaration=True,
            method="xml"
        )

        # close the file and tell the user
        outfile.close()
        print("Output is in %s" % outfilename)

########################################################################


def process(args=None):
    """Process each file in args."""

    if not args:
        args = ["topo859 - Macon County MO.gpx"]

    for arg in args:
        print("Processing: %s" % arg)
        process_arg(arg)

    print("\nProcessing complete")

########################################################################


if __name__ == '__main__':

    import argparse
    import time
    import traceback

########################################################################

    def main():
        """Main program."""

        # pylint: disable=global-statement
        global OPTIONS

        process(OPTIONS.files)

        return 0

########################################################################

    try:
        START_TIME = time.time()

        PARSER = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        PARSER.add_argument(
            "--version",
            action="version",
            version="%%(prog)s, Version: %s %s" % (__VERSION__, __DATE__)
            )

        PARSER.add_argument(
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        PARSER.add_argument(
            'files',
            action='append',
            help='specify files to be processed',
        )

        OPTIONS = PARSER.parse_args()

        if OPTIONS.verbose:
            print(time.asctime())

        EXIT_CODE = main()

        if EXIT_CODE is None:
            EXIT_CODE = 0

        if OPTIONS.verbose:
            print(time.asctime())
            print('TOTAL TIME IN MINUTES:')
            print((time.time() - START_TIME) / 60.0)

        sys.exit(EXIT_CODE)

    except KeyboardInterrupt as error_exception:        # Ctrl-C
        raise error_exception

    except SystemExit as error_exception:               # sys.exit()
        raise error_exception

    # except Exception as error_exception:
    #     print('ERROR, UNEXPECTED EXCEPTION')
    #     print(str(error_exception))
    #     traceback.print_exc()
    #     os._exit(1)

# end of file
