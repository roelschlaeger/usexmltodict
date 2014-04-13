#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Sun 13 Apr 2014 05:49:16 PM CDT
# Last Modified: Sun 13 Apr 2014 06:00:30 PM CDT

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

CROSSWORD = """
LOCK.MADAM.GNAW
OGRE.ABOVE.RAGA
ALAR.NEGOTIATOR
DEPOSIT.WARFARE
...SPA....ATLAS
IMPEACHMENT....
TEENY.EERIE.MAT
ERNE.FATAL.LAMA
MET.MOTET.SIGIL
....APHRODISIAC
SHOPS....ALT...
PATROLS.LITERAL
INTONATION.ROLE
EDEN.DUCAT.IOTA
LYRE.ENEMY.AMOK
"""

CONVERSION = {}


def convert(a, b, v):
    for c in range(ord(a), ord(b) + 1):
        CONVERSION[chr(c)] = v

convert('A', 'C', '1')
convert('D', 'F', '2')
convert('G', 'I', '3')
convert('J', 'L', '4')
convert('M', 'O', '5')
convert('P', 'R', '6')
convert('S', 'U', '7')
convert('V', 'W', '8')
convert('X', 'X', '9')
convert('Y', 'Z', '0')

# from pprint import pprint
# pprint(CONVERSION)
# pprint(CROSSWORD.split('n'))


def solve():
    lines = (CROSSWORD.split('\n'))[1:-1]
    for line in lines:
        line = line.replace('\n','')
        print line
        out = []
        for c in line:
            out.append(CONVERSION.get(c, ' '))
        print "".join(out)
        print

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

        solve()

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
