#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SYNOPSIS

    TODO venter_dna [-h] [-v,--verbose] [--version] [-d] [-e] {string string...}

DESCRIPTION

    TODO This describes how to use this script.
    This docstring will be printed by the script if there is an error or
    if the user requests help (-h or --help).

EXAMPLES

    TODO: Show some examples of how to use this script.

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Name <name@example.org>

LICENSE

    This script is in the public domain.

VERSION

"""

import sys
import os
import traceback
import optparse
import time
from watermarks import watermarks
#from pexpect import run, spawn

# Uncomment the following section if you want readline history support.
#import readline, atexit
#histfile = os.path.join(os.environ['HOME'], '.TODO_history')
#try:
#    readline.read_history_file(histfile)
#except IOError:
#    pass
#atexit.register(readline.write_history_file, histfile)

# the encoded alphabet in tabular order
alphabet = r"""C07;#UGNQHETV@AZ1+YO\-/8R=M.I):<D23B$&L> P{4*[}]JS%XW6(F9K'",5!
"""
# print len(alphabet)
# print alphabet
# print "'%s'" % alphabet

# the nucleobases in order
acids = "TCAG"

#######################################################################

def reformat(s, n):

    strings = []
    while s:
        out, s = s[:n], s[n:]
        strings.append(out)
    return "\n".join(strings)

#######################################################################

def encode(arg):
    out = []
    for c in arg:
        if c in alphabet:
            index = alphabet.index(c)
            row, column = divmod(index, 4)
            group, row = divmod(row, 4)
            out.append("%c%c%c" % (acids[group], acids[column], acids[row]))
            if options.debug:
                print c, index, group, row, column 
    return "".join(out)

#######################################################################

def decode(arg):

#   print arg
    out = []
    while len(arg) >= 3:
        triple, arg = arg[:3],arg[3:]
        (c1, c2, c3) = triple
        if c1 in acids and c2 in acids and c3 in acids:
            group = acids.find(c1)
            column = acids.find(c2)
            row = acids.find(c3)
            if group < 0 or row < 0 or column < 0:
                group = row = column = 0
            index = column + row*4 + group*16
            char = alphabet[ index ]
            if options.debug:
                print triple, group, row, column, index, char
            out.append( char )
    return "".join(out)

#######################################################################

def main ():

    global options, args

    if not args:
        import string
        if options.encode:
            args = [ string.digits + string.uppercase + string.punctuation ]
        else:
            args = [ "TCTCTTACTAATAGAGCGGCCTATCGCGTATAGAGTTTTATTTAAGGCTACTCAGTTGCAAACCAATGCCGTACATTACTAGCTTGATCCTTGGTCGGTCATTGGGAGGGATTCATCGATACCGAAGACCCGATGCCTGTGCCCCGACACCAGTGTCGGCCAAGCTCGACGCTCAGGAAACTGAAG" ]

    for arg in args:
        print arg    
        print
        arg = arg.upper()
        if options.decode:
            print decode(arg)
        else:
            s = encode(arg)
            print reformat(s, 48)
            print
            print decode(s).lower()
        print

#######################################################################

if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = optparse.OptionParser(
                formatter=optparse.TitledHelpFormatter(),
                usage=globals()['__doc__'],
                version='$Id: py.tpl 332 2008-10-21 22:24:52Z root $')
        parser.add_option (
                '-v', '--verbose', action='store_true', default=False, help='verbose output'
                )
        parser.add_option (
                '-d', '--decode', action='store_true', default=False, help='decode input strings'
                )
        parser.add_option (
                '-e', '--encode', action='store_true', default=False, help='encode input strings'
                )
        parser.add_option (
                '-D', '--debug', action='store_true', default=False, help='set debug flag'
                )        
        parser.add_option (
                '-w', '--watermark', action='store', type=int, default=-1, help='decode a watermark pattern, 1-4'
                )        
        (options, args) = parser.parse_args()

        # resolve into either encode or decode
        if not options.decode and not options.encode:
            options.encode = True

        # check for too many options
        if options.decode and options.encode:
            raise ValueError("Cannot both encode and decode")

        # check for watermark selection
        if options.watermark != -1:
            options.decode = True
            options.encode = False
            index = options.watermark
            if index < len(watermarks):
                args = [ watermarks[ index ] ]
            else:
                raise ValueError("Invalid watermark number")
                
        #if len(args) < 1:
        #    parser.error ('missing argument')
        if options.verbose: print time.asctime()
        exit_code = main()
        if exit_code is None:
            exit_code = 0
        if options.verbose: print time.asctime()
        if options.verbose: print 'TOTAL TIME IN MINUTES:',
        if options.verbose: print (time.time() - start_time) / 60.0
        sys.exit(exit_code)
    except KeyboardInterrupt, e: # Ctrl-C
        raise e
    except SystemExit, e: # sys.exit()
        raise e
    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

 # vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
