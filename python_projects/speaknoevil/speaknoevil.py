#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Sun 13 Apr 2014 01:53:27 PM CDT
# Last Modified: Sun 13 Apr 2014 02:01:53 PM CDT

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

TEXT = """
Tango hotel india romeo tommy yankee november in nuts echo delta edward golf rainbo easy edison sierra nope ortho raid tummy hippy foxrot item fred toni yellow turn wow oscar alpha nan dentist stink extra vehicle eight nick henry uniform nickel dora red elephant dog near indigo neat eats the yak zebra elevator roma okay
End ill goat hot table yoda elk ink gal hand tank dad elevate grind read ear enable sail wash eggshells stab turkey frank opal repel young ton okra apple new did next ice nine escargot hungry up now dart ran ended dear twig words escape not twirl yang zulu emotions rub ogre
"""
""" Solution to geocache at
http://www.geocaching.com/geocache/GC34N8Y_speak-no-evil?guid=c5f09576-a624-4d22-b708-f47ebef81e2b
"""

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

        textlines = TEXT.split('\n')[1:3]
#       print textlines

        for text in textlines:
            out = []
            for word in text.split():
                out.append(word[0])
            print "".join(out)

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
