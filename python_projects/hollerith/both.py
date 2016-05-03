#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Tue 03 May 2016 11:22:03 AM CDT
# Last Modified: Tue 03 May 2016 03:20:50 PM CDT

"""
SYNOPSIS

    TODO helloworld [-h | --help] [-v | --version] [--verbose]

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

from read_image import read_image, LATITUDE_IMAGE, LONGITUDE_IMAGE
from read_image import MY_LATITUDE_IMAGE
from im2holl import image_to_hollerith, hollerith_to_strings


def process_one(image, sname):
    one_list = read_image(image)
    one_hollerith = image_to_hollerith(one_list)
    one_string = hollerith_to_strings(one_hollerith)
    print(r'%s = """' % sname)
    for s in one_string:
        print s
    print(r'"""')

def process():

#   process_one(LATITUDE_IMAGE, "LATITUDE")
#   process_one(LONGITUDE_IMAGE, "LONGITUDE")
    process_one(MY_LATITUDE_IMAGE, "MY_LATITUDE")

#   lat_list = read_image(LATITUDE_IMAGE)
#   lat_hollerith = image_to_hollerith(lat_list)
#   lat_string = hollerith_to_strings(lat_hollerith)
#   print(r'LATITUDE = """')
#   for s in lat_string:
#       print s
#   print(r'"""')

#   lon_list = read_image(LONGITUDE_IMAGE)
#   lon_hollerith = image_to_hollerith(lon_list)
#   lon_string = hollerith_to_strings(lon_hollerith)
#   print(r'LONGITUDE = """')
#   for s in lon_string:
#       print s
#   print(r'"""')

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

        process()

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

        OPTIONS = PARSER.parse_args()

        if OPTIONS.verbose:
            print time.asctime()

        EXIT_CODE = main()

        if EXIT_CODE is None:
            EXIT_CODE = 0

        if OPTIONS.verbose:
            print time.asctime()
            print 'TOTAL TIME IN MINUTES:',
            print (time.time() - START_TIME) / 60.0

        sys.exit(EXIT_CODE)

    except KeyboardInterrupt, error_exception:        # Ctrl-C
        raise error_exception

    except SystemExit, error_exception:               # sys.exit()
        raise error_exception

    except Exception, error_exception:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(error_exception)
        traceback.print_exc()
        os._exit(1)

# end of file
