#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 10 Aug 2016 04:26:51 PM CDT
# Last Modified: Thu 11 Aug 2016 07:52:26 AM CDT

"""
SYNOPSIS

    make_gs [-h | --help] [-v | --version] [--verbose] file [ file ... ]

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

__VERSION__ = "0.0.1"

########################################################################


def generate_output_filename(name):
    from os.path import split, splitext, join

    # output will be in the current directory
    dir, outname = split(name)
    root, ext = splitext(outname)

    # append "_gs" to basename
    root += "_gs"

    return join(dir, root + ext)

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
            name_text = name.text
        except AttributeError as e:
            print(e, file=sys.stderr)
            name_text = "None"

        # get UserSort value
        try:
            extensions = wpt.find(extensions_tag)
            gsak = extensions.find(gsak_tag)
            usersort = gsak.find(gsak.tag.replace("wptExtension", "UserSort"))
            usersort_text = usersort.text
        except AttributeError as e:
            print(e, file=sys.stderr)
            usersort_text = "None"

        # compute a new name
        new_name = "%s %s" % (usersort_text, name_text)
        name.text = str(new_name)

    # create the modified output filename
    outfilename = generate_output_filename(arg)

    # create the binary file
    outfile = open(outfilename, "wb")

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

#   tree.write(outfilename)

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

# print(globals()['__doc__'])

if __name__ == '__main__':

    import argparse
    import os
    import sys
    import textwrap
    import time
    import traceback

#from pexpect import run, spawn

# Uncomment the following section if you want readline history support.
#import readline, atexit
#histfile = os.path.join(os.environ['HOME'], '.TODO_history')
#try:
#    readline.read_history_file(histfile)
#except IOError:
#    pass
#atexit.register(readline.write_history_file, histfile)

########################################################################

    def main():

        global OPTIONS

        process(OPTIONS.files)

########################################################################

    try:
        START_TIME = time.time()

        PARSER = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            usage=textwrap.dedent(globals()['__doc__']),
            version="Version: %s" % __VERSION__
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

    except Exception as error_exception:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(error_exception))
        traceback.print_exc()
        os._exit(1)

# end of file
