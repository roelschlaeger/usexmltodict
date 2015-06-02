#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 08 Oct 2014 08:31:13 PM CDT
# Last Modified: Wed 07 Jan 2015 03:48:58 PM CST

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

########################################################################

# rename files
# IMG_20141008_060140_436.jpg 1008140601.jpg
# IMG_20141008_070341_068.jpg
# .
# .
# .
# IMG_20141008_172436_964.jpg
# IMG_20141008_173406_904.jpg 1008141734.jpg

from exif_rename import ensure_unique


def img_rename(base, date):

    namelist = {}
    print "img_rename(%s, %s)" % (base, date)
    directory = os.path.join(base, date)
    print directory
    filenames = os.listdir(directory)
    for filename in filenames:
        root, ext = os.path.splitext(filename)
        if ext == ".jpg":
            head, tail = os.path.split(root)
#           print tail
            img, date, time, milliseconds = tail.split("_")
#           print date, time
            yr, mo, da = date[:4], date[4:6], date[6:]
            hr, mn, sc = time[:2], time[2:4], time[4:]
#           print yr, mo, da, hr, mn, sc
            name = "%2s%2s%2s%2s%2s.jpg" % (mo, da, yr[2:], hr, mn)
            unique_name = ensure_unique(name, namelist)
            print "%-20s: %-20s: %-20s" % (tail, name, unique_name)
            namelist[unique_name] = tail

    return namelist



def create_batch_file(base, date, directory_name):
    namelist = img_rename(base, date)
    outname = os.path.join(base, date, "rename_batch.bat")
    print outname

    outfile = open(outname, "w")
    print >> outfile, "mkdir %s" % directory_name
    for key in sorted(namelist):
        value = namelist[key]
        print >> outfile, r"copy %s.jpg %s\%s" % (value, directory_name, key)
    outfile.close()

########################################################################

if __name__ == '__main__':

    import sys
    import os
    import traceback
    import optparse
    import time

    BASE = "C:/Users/Robert Oelschlaeger/Google Drive/Caching Pictures"
    DATE = "x20150106"
#   DIRECTORY_NAME = "20150106"
    DIRECTORY_NAME = "20150106"

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

        global options, args

        # TODO: Do something more interesting here...
        print 'Hello world!'

        create_batch_file(BASE, DATE, DIRECTORY_NAME)

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