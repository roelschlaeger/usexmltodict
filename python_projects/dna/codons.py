#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Fri 04 Apr 2014 02:20:32 PM CDT
# Last Modified: Fri 04 Apr 2014 03:38:55 PM CDT

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

"""http://en.wikipedia.org/wiki/DNA_codon_table"""

CODONS = {
    "TTT": "(Phe/F) Phenylalanine",
    "TTC": "(Phe/F) Phenylalanine",
    "TTA": "(Leu/L) Leucine",
    "TTG": "(Leu/L) Leucine",
    "CTT": "(Leu/L) Leucine",
    "CTC": "(Leu/L) Leucine",
    "CTA": "(Leu/L) Leucine",
    "CTG": "(Leu/L) Leucine",
    "ATT": "(Ile/I) Isoleucine",
    "ATC": "(Ile/I) Isoleucine",
    "ATA": "(Ile/I) Isoleucine",
    "ATG": "(Met/M) Methionine",
    "GTT": "(Val/V) Valine",
    "GTC": "(Val/V) Valine",
    "GTA": "(Val/V) Valine",
    "GTG": "(Val/V) Valine",
    "TCT": "(Ser/S) Serine",
    "TCC": "(Ser/S) Serine",
    "TCA": "(Ser/S) Serine",
    "TCG": "(Ser/S) Serine",
    "CCT": "(Pro/P) Proline",
    "CCC": "(Pro/P) Proline",
    "CCA": "(Pro/P) Proline",
    "CCG": "(Pro/P) Proline",
    "ACT": "(Thr/T) Threonine",
    "ACC": "(Thr/T) Threonine",
    "ACA": "(Thr/T) Threonine",
    "ACG": "(Thr/T) Threonine",
    "GCT": "(Ala/A) Alanine",
    "GCC": "(Ala/A) Alanine",
    "GCA": "(Ala/A) Alanine",
    "GCG": "(Ala/A) Alanine",
    "TAT": "(Tyr/Y) Tyrosine",
    "TAC": "(Tyr/Y) Tyrosine",
    "TAA": "Stop (Ochre)",
    "TAG": "Stop (Amber)",
    "CAT": "(His/H) Histidine",
    "CAC": "(His/H) Histidine",
    "CAA": "(Gln/Q) Glutamine",
    "CAG": "(Gln/Q) Glutamine",
    "AAT": "(Asn/N) Asparagine",
    "AAC": "(Asn/N) Asparagine",
    "AAA": "(Lys/K) Lysine",
    "AAG": "(Lys/K) Lysine",
    "GAT": "(Asp/D) Aspartic acid",
    "GAC": "(Asp/D) Aspartic acid",
    "GAA": "(Glu/E) Glutamic acid",
    "GAG": "(Glu/E) Glutamic acid",
    "TGT": "(Cys/C) Cysteine",
    "TGC": "(Cys/C) Cysteine",
    "TGA": "Stop (Opal)",
    "TGG": "(Trp/W) Tryptophan",
    "CGT": "(Arg/R) Arginine",
    "CGC": "(Arg/R) Arginine",
    "CGA": "(Arg/R) Arginine",
    "CGG": "(Arg/R) Arginine",
    "AGT": "(Ser/S) Serine",
    "AGC": "(Ser/S) Serine",
    "AGA": "(Arg/R) Arginine",
    "AGG": "(Arg/R) Arginine",
    "GGT": "(Gly/G) Glycine",
    "GGC": "(Gly/G) Glycine",
    "GGA": "(Gly/G) Glycine",
    "GGG": "(Gly/G) Glycine",
}

TRANSLATOR = {
    "Ala/A": ["GCT", "GCC", "GCA", "GCG"],
    "Leu/L": ["TTA", "TTG", "CTT", "CTC", "CTA", "CTG"],
    "Arg/R": ["CGT", "CGC", "CGA", "CGG", "AGA", "AGG"],
    "Lys/K": ["AAA", "AAG"],
    "Asn/N": ["AAT", "AAC"],
    "Met/M": ["ATG"],
    "Asp/D": ["GAT", "GAC"],
    "Phe/F": ["TTT", "TTC"],
    "Cys/C": ["TGT", "TGC"],
    "Pro/P": ["CCT", "CCC", "CCA", "CCG"],
    "Gln/Q": ["CAA", "CAG"],
    "Ser/S": ["TCT", "TCC", "TCA", "TCG", "AGT", "AGC"],
    "Glu/E": ["GAA", "GAG"],
    "Thr/T": ["ACT", "ACC", "ACA", "ACG"],
    "Gly/G": ["GGT", "GGC", "GGA", "GGG"],
    "Trp/W": ["TGG"],
    "His/H": ["CAT", "CAC"],
    "Tyr/Y": ["TAT", "TAC"],
    "Ile/I": ["ATT", "ATC", "ATA"],
    "Val/V": ["GTT", "GTC", "GTA", "GTG"],
    "START": ["ATG"],
    "STOP/X": ["TAA", "TGA", "TAG"]
}

INVERSE_CODONS = {}

def prep():
    global INVERSE_CODONS

    for k, values in TRANSLATOR.items():
        for v in values:
            INVERSE_CODONS[v] = k

prep()

if __name__ == '__main__':

    import sys
    import os
    import traceback
    import optparse
    import time
    from pprint import pprint

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

        print "CODONS"
        pprint(CODONS)

        print "INVERSE_CODONS"
        pprint(INVERSE_CODONS)

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
