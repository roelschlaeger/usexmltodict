#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Tue 26 Aug 2014 09:05:21 PM CDT
# Last Modified: Wed 27 Aug 2014 11:44:03 AM CDT

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

FILENAME = "data.txt"
"""The input filename"""

########################################################################


def process_cols(line):
    """Collect the float values from a table line"""

    return map(float, line.split()[2:])

########################################################################


def grab_data(filename):
    """Collect data from FILENAME, extracting identifying information and table
    values"""

    values = []
    state = 0
    print >>sys.stderr, "reading from %s" % filename
    f = open(filename, "r")

    for line in f.readlines():

        if state == 0 and line.startswith("Application"):
            print line[:-1]
            continue
        if state == 0 and line.startswith("Version"):
            print line[:-1]
            continue
        if state == 0 and line.startswith("Build"):
            print line[:-1]
            continue
        if state == 0 and line == "rom_harmonize_data\n":
            print
            state = 1
            continue

        if state == 1 and line == "==================\n":
            state = 2
            continue

        if state == 2 and line == "\n":
            state = 3
            continue

        if state == 3:
            if line.startswith("cols"):
                values.extend(process_cols(line))
            else:
                state = 4
            continue

        if state == 4:
            break

    return values

########################################################################


def print_values(yvalues):
    """Reformat yvalues in support of generating chart"""

    xvalues = range(0, 360, 4)

    print "Angle\tValue"

    for x, y in zip(xvalues, yvalues):
        print "%d\t%f" % (x, y)

########################################################################

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

    def main():

        global options, args

        values = grab_data(FILENAME)
        print_values(values)

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
