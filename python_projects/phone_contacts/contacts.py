#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Fri 10 Oct 2014 03:23:36 PM CDT
# Last Modified: Fri 10 Oct 2014 06:42:14 PM CDT

"""
SYNOPSIS

    python contacts.py
        [-h]
        [-v,--verbose]
        [--version]
        [-b, -base <directory>]
        [-f, --file <filename>]
        [-g, --google]
        [-a, --analyze]

DESCRIPTION

    This script processes an address book .csv input file, generating a
    corresponding .csv output file with some duplicates merged.

    This docstring will be printed by the script if there is an error or if the
    user requests help (-h or --help).

EXAMPLES

    python contacts.py  # processes FILENAME in BASE directory

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

from collections import defaultdict, OrderedDict
import csv
import os.path
import re

ATT_KEY_ITEMS_LIST = [
    "First Name",
    "Middle Name",
    "Last Name",
]

GOOGLE_KEY_ITEMS_LIST = [
    "Name Prefix",
    "Given Name",
    "Family Name",
    "Name Suffix",
]

ATT_NEW_ITEMS_LIST = [
    "E-mail Address",
    "E-mail 2 Address",
    "E-mail 3 Address",
    "Primary Phone",
    "Home Phone",
    "Home Phone 2",
    "Mobile Phone",
    "Business Phone",
    "Other Phone",
    "Company",
    "Business Fax",
    "Notes",
    "Other Street",
]

GOOGLE_NEW_ITEMS_LIST = [
    "Additional Name",
    "Address 1 - Formatted",
    "Address 1 - Street",
    "Address 1 - Type",
    "E-mail 1 - Type",
    "E-mail 1 - Value",
    "E-mail 2 - Type",
    "E-mail 2 - Value",
    "Family Name",
    "Given Name",
    "Group Membership",
    "Name",
    "Name Prefix",
    "Name Suffix",
    "Notes",
    "Organization 1 - Name",
    "Phone 1 - Type",
    "Phone 1 - Value",
    "Phone 2 - Type",
    "Phone 2 - Value",
    "Phone 3 - Type",
    "Phone 3 - Value",
    "Phone 4 - Type",
    "Phone 4 - Value",
]


def merge(new_catalog, newkey, newdict):

#   print "merge(%s, %s, %s)" % (new_catalog, newkey, newdict)

#   print type(newkey), type(newdict)

    # look for newkey already in catalog
    if newkey in new_catalog:

        # merge the old data into the new
        olddict = new_catalog[newkey]
        for item in NEW_ITEMS_LIST:
            if not newdict[item]:
                newdict[item] = olddict[item]

    new_catalog[newkey] = newdict


def analyze(base, filename):

    print "analyze(%s, %s)" % (base, filename)

    csvfilename = os.path.join(base, filename)
    csvfile = open(csvfilename, "rb")
    reader = csv.DictReader(csvfile)

    sets = defaultdict(list)
#   new_catalog = defaultdict(dict)

    for row in reader:

        for fieldname in reader.fieldnames:
            sets[fieldname].append(row[fieldname])

#       newkey = " ".join([
#           row[item] for item in KEY_ITEMS_LIST
#       ])
#       newkey = re.sub("  *", " ", newkey)

#       newdict = OrderedDict(
#           zip(
#               NEW_ITEMS_LIST,
#               [row[item] for item in NEW_ITEMS_LIST]
#           )
#       )

#       print "newkey = %s" % newkey,
#       print "newdict = %s" % newdict

#       merge(new_catalog, newkey, newdict)

    # get the longest key length
    longest_key_length = max([len(s) for s in sets.keys()])

    # set up the format string
    format = "%%%ds %%3d %%s" % (longest_key_length + 1)

    # show the keys
    for key in sorted(sets):
        s = set(sets[key])
        print format % (key, len(s), str(s)[:60])

    csvfile.close()
#   return new_catalog


def process(base, filename):

    print "process(%s, %s)" % (base, filename)

    csvfilename = os.path.join(base, filename)
    csvfile = open(csvfilename, "rb")
    reader = csv.DictReader(csvfile)

#   sets = defaultdict(list)
    new_catalog = defaultdict(dict)

    for row in reader:

#       for fieldname in reader.fieldnames:
#           sets[fieldname].append(row[fieldname])

        newkey = " ".join([
            row[item] for item in KEY_ITEMS_LIST
        ])
        newkey = re.sub("  *", " ", newkey)

        newdict = OrderedDict(
            zip(
                NEW_ITEMS_LIST,
                [row[item] for item in NEW_ITEMS_LIST]
            )
        )

#       print "newkey = %s" % newkey,
#       print "newdict = %s" % newdict

        merge(new_catalog, newkey, newdict)

    # get the longest key length
#   longest_key_length = max([len(s) for s in sets.keys()])

    # set up the format string
#   format = "%%%ds %%3d %%s" % (longest_key_length + 1)

    # show the keys
#   for key in sorted(sets):
#       s = set(sets[key])
#       print format % (key, len(s), str(s)[:60])

    csvfile.close()
    return new_catalog


def display_new_catalog(new_catalog):

    print
    print "Name," + ",".join(NEW_ITEMS_LIST)
    for key in sorted(new_catalog):
        print key, new_catalog[key].values()
    print


def create_csv_file(new_catalog):

    OUTFILENAME = "contacts_out.csv"
    print "Writing to %s" % OUTFILENAME
    outfile = open(OUTFILENAME, "wb")
    writer = csv.writer(outfile)

    writer.writerow(["Name"] + NEW_ITEMS_LIST)
    for key in sorted(new_catalog):
        writer.writerow([key] + new_catalog[key].values())

    outfile.close()


def job(base, filename, analyze_flag=False):

    if analyze_flag:
        analyze(base, filename)

    else:
        new_catalog = process(base, filename)
#       display_new_catalog(new_catalog)
        create_csv_file(new_catalog)

########################################################################

BASE = "C:\Users\Robert Oelschlaeger\Downloads"

# FILENAME = "All_Contacts_Thu_Oct_09_18-42-42_CDT_2014.csv"
# FILENAME = "All_Contacts_Thu_Oct_09_18-42-42_CDT_2014_EDITED.csv"
# FILENAME = "google_contacts.csv"
FILENAME = "contacts.csv"

if __name__ == '__main__':

    import sys
    import os
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

    def main(args, options):

        base = options.base
        filename = options.filename
        analyze_flag = options.analyze

        print "main(%s, %s)" % (args, options)

        job(base, filename, analyze_flag)

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
            '-b',
            '--base',
            action='store',
            default=BASE,
            help='set base file reading directory, default: %default'
        )

        PARSER.add_option(
            '-f',
            '--filename',
            action='store',
            default=FILENAME,
            help='set filename; default: %default'
        )

        PARSER.add_option(
            '-g',
            '--google',
            action='store_true',
            default=False,
            help='set Google flag'
        )

        PARSER.add_option(
            '-a',
            '--analyze',
            action='store_true',
            default=False,
            help='set analyze_flag'
        )

        (OPTIONS, ARGS) = PARSER.parse_args()

        if OPTIONS.google:
            NEW_ITEMS_LIST = GOOGLE_NEW_ITEMS_LIST
            KEY_ITEMS_LIST = GOOGLE_KEY_ITEMS_LIST
        else:
            NEW_ITEMS_LIST = ATT_NEW_ITEMS_LIST
            KEY_ITEMS_LIST = ATT_KEY_ITEMS_LIST

        if OPTIONS.verbose:
            print time.asctime()

        EXIT_CODE = main(ARGS, OPTIONS)

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
