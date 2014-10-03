#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 02 Oct 2014 06:37:29 PM CDT
# Last Modified: Thu 02 Oct 2014 11:53:39 PM CDT

"""
SYNOPSIS

    TODO helloworld [-h] [-v,--verbose] [--version]

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

#######################################################################

import exifread
from itertools import chain, count
import os
import string

#########################################################################


def ensure_unique(name, namelist):
    """return unique name not already in namelist"""

    # separate root from extension
    root, ext = os.path.splitext(name)

    # set up potential name modifier
    g = chain(string.lowercase, count())

    # start with original name
    testname = root

    # check for name alread in namelist
    while testname + ext in namelist:

        # creaste a new modified name
        testname = "%s%s" % (root, g.next())

    # return the result with its extension
    return testname + ext

if 0:
    namelist = {}
    for x in range(100):
        y = ensure_unique('test.jpg', namelist)
        namelist[y] = x
        print y

    import sys
    sys.exit(0)

#########################################################################


def process(path, debug=False):
    """Process .jpg files in the path directory"""

    if debug:
        print "process(%s, debug=%s)" % (path, debug)

    # return the dictionary of filename:newname values
    translation_table = {}

    # get the list of files
    filenames = os.listdir(path)

    # examine each file in the directory
    for filename in filenames:

        # looking only at the .jpg files
        if filename.endswith('.jpg'):

            if debug:
                print filename

            # form the complete pathname
            pathname = os.path.join(PATH, filename)

            # open the file for reading EXIF data
            f = open(pathname, "rb")

            # read the EXIF tags
            tags = exifread.process_file(f)

            # optionally show the results
            if debug:

                # show all of the relevant keys
                for tag in tags.keys():

                    if tag not in (
                        'JPEGThumbnail',
                        'TIFFThumbnail',
                        'Filename',
                        'EXIF MakerNote'
                    ):
                        print "%-38s: %s" % (tag, tags[tag])

            # we're interested in the original date and time the picture was
            # taken
            datetimeoriginal = str(tags["EXIF DateTimeOriginal"])

            # split into date and time fields
            date, time = datetimeoriginal.split()
            if debug:
                print "Date: %s Time: %s" % (date, time)

            # split into year, month, day, hour, minute, second fields
            yr, mo, dy = date.split(":")
            hr, mn, se = time.split(":")

            # generate a new name like the old camera used to make
            newname = "%2s%2s%2s%2s%2s.jpg" % (mo, dy, hr, mn, se)

            uniquename = ensure_unique(newname, translation_table.keys())

            if debug:
                print yr, mo, dy, hr, mn, se, newname, uniquename

            # put an entry into the table
            translation_table[uniquename] = filename

            if debug:
                print

    return translation_table

if __name__ == '__main__':

    import sys
#   import os
    import traceback
    import optparse
    import time

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

    PATH = r"C:\Users\Robert Oelschlaeger\Google Drive\Caching Pictures\20141001"
    """Location of pictures containing EXIF data"""

    def main():

        global OPTIONS, ARGS

        debug = OPTIONS.debug or False

        if debug:
            print ARGS, OPTIONS
            print PATH
            print

        result = process(PATH, debug)
        from pprint import pprint
        pprint(result)

########################################################################

    try:
        START_TIME = time.time()

        PARSER = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version=__VERSION__
        )

        PARSER.add_option(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        PARSER.add_option(
            '-d',
            '--debug',
            action='store_true',
            default=False,
            help='debug'
        )

        (OPTIONS, ARGS) = PARSER.parse_args()

        #   if len(ARGS) < 1:
        #       PARSER.error ('missing argument')

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
