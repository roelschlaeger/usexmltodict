#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Sun 13 Apr 2014 02:25:23 PM CDT
# Last Modified: Sun 13 Apr 2014 02:36:49 PM CDT

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

CIPHERTEXT = [
    '011110', '101100', '011000', '101110', '011110', '110111', '110110',
    '011000', '110110', '100100', '110100', '100100', '111100', '101110',
    '100100', '100100', '011010', '111000', '011000', '111000', '011110',
    '110111', '011110', '011101', '100110', '110100', '100110', '011110',
    '110110', '011000', '110110', '100100', '011010', '011000', '110011',
    '100100', '011000', '111100', '101100', '011110', '100100', '011000',
    '111100', '101100', '011110', '110111', '100100', '011000', '111100',
    '101100', '011110', '110100', '100100', '111100', '101110', '100100',
    '100100', '011010', '111000', '100110', '100011', '101110', '011110',
    '101100', '101110', '100100', '100100', '110100', '100110', '011110',
    '110110', '011000', '110110', '100100', '011010', '011000', '110011',
    '111000', '011000', '101011', '100100'
]

from collections import Counter
c = Counter(CIPHERTEXT)

from pprint import pprint
pprint(c)

# TRANSLATOR = { '100100': 'E', }

from string import uppercase
TRANSLATOR = dict(zip(c.keys(), uppercase[:len(c.keys())]))

print "".join([TRANSLATOR.get(c, "?") for c in CIPHERTEXT])

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

        # TODO: Do something more interesting here...
        print 'Hello world!'

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
