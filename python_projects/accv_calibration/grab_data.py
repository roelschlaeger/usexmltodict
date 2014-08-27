#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Tue 26 Aug 2014 09:05:21 PM CDT
# Last Modified: Wed 27 Aug 2014 04:40:30 PM CDT

"""
SYNOPSIS

    python grab_data.py
        [-h, --help]
        [-v, --verbose]
        [--version]
        [[-o, --output] output_filename]
        [input_filename]

DESCRIPTION

    This script collects calibration information from a text file containing
    formatted ACCV data and reformats it in a form suitable for input to a
    spreadsheet program.

    If *input_filename* is not provided, "data.txt" is used.

EXAMPLES

    python grab_data.py output_file.csv

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

"""

__VERSION__ = "0.0.2"

########################################################################

FILENAME = "data.txt"
"""The default input filename"""

#   """
#   Application: ACCV_BLDC
#   Version:     0.2.8.11
#   Build:       20131029
#
#                                                  Harmonize
#                             Program State         Offset
#                       =========================  =========
#                       ALL    MTR1    MTR2_AXIAL
#                       ------ ------  ----------  --------
#   rom_harmonize_data: 0x0000 0x0000    0x0000     0x55fc
#                       \_____________________/
#                                  |
#                               0xffff = Unprogrammed
#                               0x0000 = Programmed
#                               0x0001 = Partly programmed
#                               0x0002 = Misprogrammed
#
#
#
#   Enter Password: Password
#
#   Select menu
#   1 - menu 1: pi_motor1_phase_detector.param
#   2 - menu 2: pi_motor1_idc.param
#   3 - menu 3: pi_motor1_rate.param
#   4 - menu 4: pi_motor2_idc.param
#   5 - menu 5: pi_motor2_position.param
#
#   6 - menu 6: Dac Channel Selection
#
#   7 - RESET
#
#   8 - DisplayHarmonizeData
#   8
#                                                  Harmonize
#                             Program State         Offset
#                       =========================  =========
#                       ALL    MTR1    MTR2_AXIAL
#                       ------ ------  ----------  --------
#   rom_harmonize_data: 0x0000 0x0000    0x0000     0x55fc
#                       \_____________________/
#                                  |
#                               0xffff = Unprogrammed
#                               0x0000 = Programmed
#                               0x0001 = Partly programmed
#                               0x0002 = Misprogrammed
#
#
#   rom_harmonize_data
#   ==================
#
#   cols 00-04:    0.177883    0.181485    0.177263    0.160720    0.140571
#   cols 05-09:    0.133563    0.132405    0.129925    0.121168    0.116266
#   cols 10-14:    0.120538    0.118764    0.113832    0.115485    0.119059
#   cols 15-19:    0.121871    0.131132    0.136865    0.130735    0.128787
#   cols 20-24:    0.136824    0.147551    0.137845    0.128611    0.128641
#   cols 25-29:    0.129177    0.117638    0.104029    0.100638    0.100562
#   cols 30-34:    0.102443    0.097816    0.097554    0.096358    0.095870
#   cols 35-39:    0.100202    0.102628    0.104137    0.104253    0.103700
#   cols 40-44:    0.111524    0.120846    0.126988    0.134905    0.143437
#   cols 45-49:    0.151411    0.155720    0.141928    0.147719    0.158419
#   cols 50-54:    0.152653    0.139366    0.128311    0.123504    0.130040
#   cols 55-59:    0.141599    0.129480    0.121493    0.124083    0.141158
#   cols 60-64:    0.139463    0.152641    0.148078    0.168555    0.168114
#   cols 65-69:    0.180351    0.201203    0.207343    0.204250    0.214174
#   cols 70-74:    0.216204    0.207271    0.193938    0.189377    0.184602
#   cols 75-79:    0.179836    0.173120    0.174890    0.166526    0.172470
#   cols 80-84:    0.167293    0.173621    0.179142    0.180672    0.189402
#   cols 85-89:    0.193476    0.191980    0.206092    0.199246    0.203260
#
#   Table 1 Average:    0.146729
#   Table 2 Average:    0.146500
#
#
#   """

########################################################################


def process_cols(line):
    """Collect the float values from a table input line"""

    return map(float, line.split()[2:])

########################################################################


def grab_data(filename):
    """Collect data from FILENAME, extracting identifying information and table
    values"""

    values = []
    state = 0
    print >>sys.stderr, "Reading from %s" % filename
    print >>sys.stderr

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
            if line.startswith("Table "):
                print line[:-1]
            else:
                print
                state = 5
            continue

        if state == 5:
            break

    assert state==5, "Missing data?"
    assert len(values) > 0, "Missing data?"

    return values

########################################################################


def print_values(outfile, xvalues, yvalues):
    """Reformat xvalues and yvalues in support of generating chart"""

    print >>outfile, "Angle\tValue"
    for x, y in zip(xvalues, yvalues):
        print >>outfile, "%d\t%f" % (x, y)

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

    def main(options, args):

        # set up input filename
        if len(args) < 1:
            filename = FILENAME
        else:
            filename = args[0]

        xvalues = range(0, 360, 4)
        yvalues = grab_data(filename)

        if options.output_filename:
            outfile = open(options.output_filename, "wb")
            print >>sys.stderr, "Writing to %s" % options.output_filename
            print >>sys.stderr
        else:
            outfile = sys.stdout

        print_values(outfile, xvalues, yvalues)

########################################################################

    try:
        START_TIME = time.time()

        PARSER = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version=__VERSION__
        )

        PARSER.add_option(
            '-o',
            '--output',
            dest="output_filename",
            action='store',
            help='set output filename (defaults to stdout)'
        )

        PARSER.add_option(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='enable verbose output'
        )

        (OPTIONS, ARGS) = PARSER.parse_args()

        if OPTIONS.verbose:
            print time.asctime()

        EXIT_CODE = main(OPTIONS, ARGS)

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
