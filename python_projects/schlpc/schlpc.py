#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 05 Feb 2014 06:26:42 PM CST
# Last Modified: Wed 05 Feb 2014 06:35:18 PM CST

"""
SYNOPSIS

    schlpc [-h] [-v,--verbose] [--version]

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
0100111000100000001100110011100000100000001100110011
0001001011100011100000110000001101110000110100001010
0101011100100000001110010011000000100000001100100011
100000101110001101100011001000110000
"""

########################################################################


def octets(s):
    print
    out = []
    outch = []
    while s:
        o, s = s[:8], s[8:]
        out.append(o)
        outch.append(chr(int(o,2)))

    print
    print "\n".join(out)
    print
    print "".join(outch)
    print

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

        text = "".join(TEXT.split("\n")[1:-1])

        print TEXT
        print
        print len(text)
        print text
        print

        octets(text)

########################################################################

    try:
        start_time = time.time()

        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version=__VERSION__
        )

        parser.add_option(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        (options, args) = parser.parse_args()

        #   if len(args) < 1:
        #       parser.error ('missing argument')

        if options.verbose:
            print time.asctime()

        exit_code = main()

        if exit_code is None:
            exit_code = 0

        if options.verbose:
            print time.asctime()
            print 'TOTAL TIME IN MINUTES:',
            print (time.time() - start_time) / 60.0

        sys.exit(exit_code)

    except KeyboardInterrupt, e:        # Ctrl-C
        raise e

    except SystemExit, e:               # sys.exit()
        raise e

    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

# end of file
