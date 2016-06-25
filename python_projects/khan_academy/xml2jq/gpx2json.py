#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Sat 25 Jun 2016 01:17:33 PM CDT
# Last Modified: Sat 25 Jun 2016 02:42:03 PM CDT

"""
SYNOPSIS

    gpx2json [-h | --help] [-v | --version] [--verbose] file [ file... ]

DESCRIPTION

    TODO Convert one or more files from .gpx to .json

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

"""

from __future__ import print_function

__VERSION__ = "0.0.1"

########################################################################

import xmltodict
import json
import os.path


def process_arg(infile_name):
    print()
    print('process_arg("', infile_name, '")', sep="")
    outfile_name = os.path.split(infile_name)[1] + ".js"
    with open(infile_name, "r") as f:
        xml = xmltodict.parse(f)
        with open(outfile_name, "w") as f2:
            print("output is in '%s'" % outfile_name)
            print(json.dumps(xml, indent=2), file=f2)


########################################################################


def process_args(args):
    print('process_args')
    for arg in args:
        process_arg(arg)

########################################################################

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

        from pprint import pprint
        pprint(OPTIONS)
        process_args(OPTIONS.files)

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
            help='one or more files to process'
        )

        OPTIONS = PARSER.parse_args()

        if OPTIONS.verbose:
            print(time.asctime())

        EXIT_CODE = main()

        if EXIT_CODE is None:
            EXIT_CODE = 0

        if OPTIONS.verbose:
            print(time.asctime())
            print('TOTAL TIME IN MINUTES:', delim=" ")
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
