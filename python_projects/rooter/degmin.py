#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Fri 17 Jan 2014 06:11:21 PM CST
# Last Modified: Mon 15 Feb 2016 05:47:49 PM CST

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

from math import trunc
import sys

assert sys.version_info > (3, ), "Python 3 required"

########################################################################

__VERSION__ = "0.0.2"
__DATE__ = "2017-07-28"

########################################################################


def degmin(latlon, posneg=" -"):
    """
    Convert a latitude or longitude in 'latlon' to a proper string formatted
    like N12 34.567 using posneg[0] as the positive value indicator, posneg[1]
    as the negative value indicator.

    For latitude,  string = degmin(lat, "NS")
    For longitude, string = degmin(lon, "EW")

    """

    _value = float(latlon)

    sign = (_value < 0)

    _value = abs(_value)

    degrees, fraction = trunc(_value), _value - trunc(_value)
    minutes = fraction * 60.
    minutes, thousandths = (
        trunc(minutes),
        trunc((minutes - trunc(minutes)) * 1000.)
    )

    # apply sign
    if sign:
        _string = posneg[1]
    else:
        _string = posneg[0]

    _string = _string.strip()
    _string += "%d %02d.%03d" % (degrees, minutes, thousandths)

    return _string

########################################################################


def latdegmin(lat):
    """Return L{lat} formatted as latitude."""
    return degmin(lat, "NS")

########################################################################


def londegmin(lon):
    """Return L{lon} formatted as longitude."""
    return degmin(lon, "EW")

########################################################################


if __name__ == '__main__':

    import argparse
    import time
    import textwrap

########################################################################

    def main():

        """Main test routine."""

        print(degmin(38.20575, "NS"))
        print(latdegmin(38.20575))

        print(degmin(-38.20575, "NS"))
        print(latdegmin(-38.20575))

        print(degmin(-90.39094, "EW"))
        print(londegmin(-90.39094))

        print(degmin(90.39094, "EW"))
        print(londegmin(90.39094))

        return 0

########################################################################

    try:
        START_TIME = time.time()

        PARSER = argparse.ArgumentParser(
            usage=textwrap.dedent(__doc__)
        )

        PARSER.add_argument(
            "--version",
            action="version",
            version="%%(prog)s, Version: %s %s" % (__VERSION__, __DATE__)
            )

        PARSER.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        OPTIONS = PARSER.parse_args()
        ARGS = None

        #   if len(args) < 1:
        #       PARSER.error ('missing argument')

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
