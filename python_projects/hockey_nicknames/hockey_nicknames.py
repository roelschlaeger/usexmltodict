#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 05 Jun 2014 11:36:10 AM CDT
# Last Modified: Thu 05 Jun 2014 12:01:38 PM CDT

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

"""
http://www.tmlfever.com/nicknames.html
http://en.wikipedia.org/wiki/List_of_ice_hockey_nicknames
http://books.google.com/books?id=rXlayAtOWjQC
http://www.hockey-reference.com/

 9 - "The Rocket" (All Years) - Maurice Richards - http://en.wikipedia.org/wiki/Maurice_Richard
25 - "Battleship" (1978-1979) - Bob Kelly -
 1 - "Suitcase" (1966) - Gary Smith -
12 - "The Roadrunner" (All Years) - Yvan Cournoyer -
31 - "Cujo" (All Years) - Curtis Joseph -
30 - "Bones" (1980) - Bronco Horvath -
16 - "The Jet" (1969) - Eddie Joyal -
 5 - "King Kong" (1980) - Jerry Korab
21 - "Seldom" (All Years) - Frank Beaton -
14 - "Murder" (1982) - Don Murdoch -
15 - "Captain Crunch" (1977) - (Gilles Marotte, Wendel Clark, Michael Peca, Scott Stevens) -
30 - "Cheesie" (1970) - Gerry Cheevers -
13 - "The Rat" (1992) - Ken Linseman -
17 - "Mr. Hockey" (1947) - Gordie Howe? -
66 - "Super Mario" (All Years) - Mario Lemeieux -
99 - "The Great One" (All Years) - Wayne Gretzky -
"""

TEXT = """
N 38°
("The Rocket"-"King Kong"-"Suitcase")
("Seldom"-"Murder")
.
("Mr. Hockey"-"The Rat")
("Cujo"-"Bones")
("The Jet"-"The Roadrunner")

W 090°
("The Great One"-"Super Mario"-"The Rat")
.
("Captain Crunch"-"The Rocket")
("Cheesie"-"Bones")
("Battleship"-"The Jet")
"""

FORMAT = "N38 %d%d.%d%d%d W090 %d.%d%d%d"

TABLE = {
    "The Rocket":                     9,
    "Battleship":                    25,
    "Suitcase":                       1,
    "The Roadrunner":                12,
    "Cujo":                          31,
    "Bones":                         30,
    "The Jet":                       16,
    "King Kong":                      5,
    "Seldom":                        21,
    "Murder":                        14,
    "Captain Crunch":                15,
    "Cheesie":                       30,
    "The Rat":                       13,
    "Mr. Hockey":                    17,
    "Super Mario":                   66,
    "The Great One":                 99,
}


def table(s):
    s = s.replace('"', '')
    return TABLE[s]


def process(line):
#   print line
    line = line[1:-2]
#   print line
    parts = line.split("-")
    print parts
    big = table(parts[0])
    others = [table(x) for x in parts[1:]]
    result = big - sum(others)
    print big, "-", others, "=", result
    return result

def job():
    out = []
    for line in TEXT.split("\n"):
        if not line:
            print
            continue
        if line[0] == '(':
            result = process(line)
            out.append(result)
    print FORMAT % tuple(out)

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

        job()

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
