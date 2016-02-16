#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Fri 17 Jan 2014 06:05:32 PM CST
# Last Modified: Mon 15 Feb 2016 06:00:50 PM CST

from __future__ import print_function

"""
SYNOPSIS

    TODO maplink [-h] [-v,--verbose] [--version]

DESCRIPTION

    TODO This describes how to use this script.
    This docstring will be printed by the script if there is an error or
    if the user requests help (-h or --help).

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

VERSION

"""

__VERSION__ = "0.0.1"

########################################################################

LINK = "https://www.google.com/search?q="

# was: from urllib import quote
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

from degmin import degmin

########################################################################


def maplink(lat, lon):

    dmlat = degmin(lat, "NS")
    dmlon = degmin(lon, "EW")

    return LINK + quote("%s %s" % (dmlat, dmlon))

########################################################################

if __name__ == '__main__':

    import sys
    import os
    import traceback
    import optparse
    import time

########################################################################

    def main():

        global options, args

        print(maplink(38.798867, -90.508867))

########################################################################

    try:
        start_time = time.time()

        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version=__VERSION__
        )

        parser.add_option(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        (options, args) = parser.parse_args()

        #   if len(args) < 1:
        #       parser.error ('missing argument')

        if options.verbose:
            print(time.asctime())

        exit_code = main()

        if exit_code is None:
            exit_code = 0

        if options.verbose:
            print(time.asctime())
            print('TOTAL TIME IN MINUTES:',)
            print((time.time() - start_time) / 60.0)

        sys.exit(exit_code)

    except KeyboardInterrupt as e:      # Ctrl-C
        raise e

    except SystemExit as e:             # sys.exit()
        raise e

    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        os._exit(1)

# end of file
