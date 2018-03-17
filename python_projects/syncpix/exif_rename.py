#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

from __future__ import print_function

# Created:       Thu 02 Oct 2014 06:37:29 PM CDT
# Last Modified: Sat 17 Mar 2018 10:12:41 AM CDT

#######################################################################

from itertools import chain, count
import exifread
import os
import string
from pprint import pprint, pformat
import sys

#######################################################################

"""
SYNOPSIS

    exif_rename.py
        [-h]
        [-v, --verbose]
        [--version]
        [-d, --debug]
        [[-b, --base] <base directory>]
        [[-t, --date] yyyymmdd]
        [-l{l...}]
        [--directory]

DESCRIPTION

    Convert picture filenames from 'yyyymmdd nnn.jpg' format (generated by
    camera in Android smart phone) to 'mmddhhmmss.jpg' format (generated by
    camera in Verizon flip phone).

EXAMPLES

    # use default values
    python exif_rename

    # convert for 20141001
    python exif_rename -t 20141001

    # generate a batch file
    python exif_rename -g

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

VERSION

"""

__VERSION__ = "0.1.0"

#########################################################################


def show_make_html(base):

    msg = """Display the status of directories below '%s' that contain
'explorist_results....gpx' files, indicating whether a corresponding
'make_html.html' is there also.
""" % base
    print(msg)

    for filename in sorted(os.listdir(base)):

        path = os.path.join(base, filename)
        if os.path.isdir(path):
            files = os.listdir(path)
            explorist = any([f.startswith("explorist_results") for f in files])
            if explorist:
                status = ("make_html.html" in files)
                print(filename, status)

#########################################################################


def show_directories(base, level):
    """Show the directories in the 'base' directory"""

    # get filenames in sorted order
    for filename in sorted(os.listdir(base)):

        # form the path
        path = os.path.join(base, filename)

        # check for directory
        if os.path.isdir(path):

            # get the files in the directory
            files = os.listdir(path)

            if (
                (level == 1) or
                any([f.startswith("explorist_results") for f in files])
            ):

                # show them on one line
                sfiles = str(files)
                if len(sfiles) > 60:
                    sfiles = sfiles[:56] + "...]"
                print("%-20s %3d: %s" % (filename, len(files), sfiles))

#########################################################################


def ensure_unique(name, namelist):
    """return unique name not already in namelist"""

    # separate root from extension
    root, ext = os.path.splitext(name)

    # set up potential name modifier
    g = chain(string.ascii_lowercase, count())

    # start with original name
    testname = root

    # check for name alread in namelist
    while testname + ext in namelist:

        # create a new modified name
        if sys.version_info < (3,):
            testname = "%s%s" % (root, g.next())
        else:
            testname = "%s%s" % (root, next(g))

    # return the result with its extension
    return testname + ext


if 0:
    namelist = {}
    for x in range(100):
        y = ensure_unique('test.jpg', namelist)
        namelist[y] = x
        print(y)

    sys.exit(0)

#########################################################################


def get_exif_timestamp(path, filename, debug):
    """Return year, month, day, hour, minute, second from EXIT timestamp for
(path, filename)"""

    # form the complete pathname
    pathname = os.path.join(path, filename)

    # open the file for reading EXIF data
    f = open(pathname, "rb")

    # read the EXIF tags
    tags = exifread.process_file(f)

    # optionally show the results
    if debug:

        print("tags:")

        # show all of the relevant keys
        for tag in list(tags.keys()):

            if tag not in (
                'JPEGThumbnail',
                'TIFFThumbnail',
                'Filename',
                'EXIF MakerNote'
            ):
                print("%-38s: %s" % (tag, tags[tag]))
        print()

    # we're interested in the original date and time the picture was
    # taken
    try:
        datetimeoriginal = str(tags["EXIF DateTimeOriginal"])
    except KeyError as e:
        print("Error extracting 'EXIF DateTimeOriginal' in", pathname)
        print(str(e))
        print()
#       print(e.args, e.message)
        print(e.args)
        print()
        print("SKIPPING")
        print()
        datetimeoriginal = "2001:01:01 00:00:00"

    # split into date and time fields
    date, time = datetimeoriginal.split()
    if debug:
        print("Date: %s Time: %s" % (date, time))

    # split into year, month, day, hour, minute, second fields
    yr, mo, dy = date.split(":")
    hr, mn, se = time.split(":")

    return yr, mo, dy, hr, mn, se

#########################################################################


BATFILENAME = "rename_files.bat"
"""The output filename for the batch file for renaming .jpg files"""


def generate_cmd_file(path, result, debug=False):
    """Generate a Windows batch file to copy and rename picture files to a
temporary directory"""

    if debug:
        print("generate_cmd_file(%s, %s, %s)" % (path, result, debug))

    # create the output filename
    outpath = os.path.join(path, BATFILENAME)

    if debug:
        print("Creating file %s" % outpath)

    outfile = open(outpath, "w")

    print("@rem Renaming files to include timestamp", file=outfile)

    # for all entries in the result dictionary
    for new in sorted(list(result.keys())):

        # get the old filename
        old = result[new]

        # report it
        if debug:
            print('@mv "%s" %s' % (old, new))

        # copy and rename the file to the temporary directory
        print('@mv "%s" %s' % (old, new), file=outfile)

    # close the batch file
    outfile.close()

########################################################################


def process(path, debug=False):
    """Process .jpg files in the path directory"""

    if debug:
        print("process(%s, debug=%s)" % (path, debug))
    # return the dictionary of filename:newname values
    translation_table = {}

    # get the list of files
    filenames = os.listdir(path)

    if debug:
        pprint(filenames)

    # examine each file in the directory
    for filename in filenames:

        # case agnostic
        filename = filename.lower()

        # looking only at the .jpg files
        if filename.endswith('.jpg'):

            if debug:
                print("filename = ", filename)

            # get picture date from EXIF timestamp
            yr, mo, dy, hr, mn, se = get_exif_timestamp(path, filename, debug)

            # generate a new name like the old camera used to make

            # this was the old format
#           newname = "%2s%2s%2s%2s%2s.jpg" % (mo, dy, yr[2:], hr, mn)
            newname = "IMG_%4s%2s%2s_%2s%2s%2s_000.jpg" % \
                (yr, mo, dy, hr, mn, se)

            uniquename = ensure_unique(newname, list(translation_table.keys()))

            if debug:
                print(yr, mo, dy, hr, mn, se, newname, uniquename)

            # put an entry into the table
            translation_table[uniquename] = filename

            if debug:
                print()

    return translation_table

########################################################################


if __name__ == '__main__':

    # import sys
    # import os
    import traceback
    import optparse
    import time

# from pexpect import run, spawn

# Uncomment the following section if you want readline history support.
# import readline, atexit
# histfile = os.path.join(os.environ['HOME'], '.TODO_history')
# try:
#     readline.read_history_file(histfile)
# except IOError:
#     pass
# atexit.register(readline.write_history_file, histfile)

########################################################################

    BASE = "C:/Users/Robert Oelschlaeger/Google Drive/Caching Pictures"
    """Location of pictures containing EXIF data"""

    from common_info import DATE
    """Location of this week's pictures"""

    def main():

        global OPTIONS, ARGS

        debug_option = OPTIONS.debug
        base_option = OPTIONS.base
        date_option = OPTIONS.date
        generate_option = OPTIONS.generate
        list_option = OPTIONS.list
        directory_option = OPTIONS.directory

        if debug_option:
            print("ARGS             = ", ARGS)
            print("OPTIONS          = ", pformat(OPTIONS))
            print("debug_option     = ", debug_option)
            print("base_option      = ", base_option)
            print("date_option      = ", date_option)
            print("generate_option  = ", generate_option)
            print("list_option      = ", list_option)
            print("directory_option = ", directory_option)
            print()

        if list_option:
            show_directories(base_option, list_option)
        elif directory_option:
            show_make_html(base_option)
        else:
            path = os.path.join(base_option, date_option)
            result = process(path, debug_option)
            pprint(result)

            if generate_option:
                generate_cmd_file(path, result, debug_option)

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

        PARSER.add_option(
            '-b',
            '--base',
            action='store',
            default=BASE,
            help='set base directory: default="%default"'
        )

        PARSER.add_option(
            '-t',
            '--date',
            action='store',
            default=DATE,
            help='set transit date: "%default"'
        )

        PARSER.add_option(
            '-g',
            '--generate',
            action='store_true',
            default=False,
            help='generate cmd file to cause rename'
        )

        _helpmsg = " ".join(
            [
                'list directories in the base directory; repeat for showing',
                'only directories with "explorist_results..."'
            ]
        )
        PARSER.add_option(
            '-l',
            '--list',
            action='count',
            default=0,
            help=_helpmsg
        )

        _helpmsg = " ".join(
            [
                'list directories in the base directory indicating whether',
                'they have a make_html.html file in them'
            ]
        )
        PARSER.add_option(
            '',
            '--directory',
            action='store_true',
            default=False,
            help=_helpmsg
        )

        (OPTIONS, ARGS) = PARSER.parse_args()

        if OPTIONS.verbose:
            print(time.asctime())

        EXIT_CODE = main()

        if EXIT_CODE is None:
            EXIT_CODE = 0

        if OPTIONS.verbose:
            print(time.asctime())
            print('TOTAL TIME IN MINUTES:', end=" ")
            print((time.time() - START_TIME) / 60.0)

        sys.exit(EXIT_CODE)

    except KeyboardInterrupt as error_exception:      # Ctrl-C
        raise error_exception

    except SystemExit as error_exception:             # sys.exit()
        raise error_exception

    except Exception as error_exception:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(error_exception))
        traceback.print_exc()
        os._exit(1)

# end of file
