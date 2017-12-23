#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Fri 17 Jan 2014 06:05:32 PM CST
# Last Modified: Mon 15 Feb 2016 06:00:50 PM CST

"""
DESCRIPTION

    TODO This describes how to use this script.
    This docstring will be printed by the script if there is an error or
    if the user requests help (-h or --help).

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

"""

########################################################################

from __future__ import print_function

import sys

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

from degmin import degmin

assert sys.version_info > (3, ), "Python 3 required"

########################################################################

__VERSION__ = "0.0.2"
__DATE__ = "2017-07-28"
LINK = "https://www.google.com/search?q="

########################################################################


def maplink(lat, lon):
    """Test LINK function."""

    dmlat = degmin(lat, "NS")
    dmlon = degmin(lon, "EW")

    return LINK + quote("%s %s" % (dmlat, dmlon))

########################################################################


if __name__ == '__main__':

    # import sys
    # import os
    # import traceback
    # import optparse
    import argparse
    import textwrap
    import time

########################################################################

    def main():
        """Test main() function."""

        print(maplink(38.798867, -90.508867))

        return 0

########################################################################

    try:
        START_TIME = time.time()

        PARSER = argparse.ArgumentParser(
            usage=textwrap.dedent(globals()['__doc__']),
            # formatter=optparse.TitledHelpFormatter(),
            # version=__VERSION__
        )

        PARSER.add_argument(
            '--version',
            action='version',
            version="%%(prog)s: VERSION %s %s" % (__VERSION__, __DATE__)
        )
        PARSER.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        OPTIONS = PARSER.parse_args()

        if OPTIONS.verbose:
            print(time.asctime())

        EXIT_CODE = main()

        if EXIT_CODE is None:
            EXIT_CODE = 0

        if OPTIONS.verbose:
            print(time.asctime())
            print('TOTAL TIME IN MINUTES:',)
            print((time.time() - START_TIME) / 60.0)

        sys.exit(EXIT_CODE)

    except KeyboardInterrupt as _error:      # Ctrl-C
        raise _error

    except SystemExit as _error:             # sys.exit()
        raise _error

    # except Exception as _error:
    #     print('ERROR, UNEXPECTED EXCEPTION')
    #     print(str(_error))
    #     traceback.print_exc()
    #     os._exit(1)

# end of file
