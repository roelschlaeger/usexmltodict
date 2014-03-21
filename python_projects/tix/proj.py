#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Fri 21 Mar 2014 10:45:35 AM CDT
# Last Modified: Fri 21 Mar 2014 02:35:09 PM CDT

"""
SYNOPSIS

    proj [-h] [-v,--verbose] [--version]

DESCRIPTION

    Follow-along implementation of application shown on YouTube at

    - https://www.youtube.com/watch?v=yI7NYgP54sw

EXAMPLES

    python proj.py

EXIT STATUS

    TODO: List exit codes

AUTHOR

    TODO: Robert Oelschlaeger <roelschlaeger@gmail.com>

LICENSE

    This script is in the public domain.

VERSION

"""

__VERSION__ = "1.0.1"

########################################################################

from Tkinter import *
import ttk

# Create a small application with the following layout:

# +-------------------+----------------+----------------+
# |                   | Feet to Meters |                |
# +-------------------+----------------+----------------+
# |                   | ()             | Feet           |
# +-------------------+----------------+----------------+
# | is equivalent to: | ()             | Meters         |
# +-------------------+----------------+----------------+
# |                   |                | <Calculate>    |
# +-------------------+----------------+----------------+

########################################################################


def main_sub():

    def calculate(*args):
        try:
            value = float(feet.get())
            meters.set(round(0.3048 * value, 4))
        except ValueError:
            pass

    root = Tk()
    root.title("Feet to Meters")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
    mainframe.grid(column=0, row=0, sticky=(N, E, S, W))

    feet = StringVar()
    feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
    feet_entry.grid(column=1, row=0, sticky=(W, E))

    meters = StringVar()
    ttk.Label(
        mainframe,
        textvariable=meters
    ).grid(column=1, row=1, sticky=(W, E))

    ttk.Label(
        mainframe,
        text="feet",
    ).grid(column=2, row=0, sticky=W)

    ttk.Label(
        mainframe,
        text="is equivalent to"
    ).grid(column=0, row=1, sticky=E)

    ttk.Label(
        mainframe,
        text="meters"
    ).grid(column=2, row=1, stick=W)

    ttk.Button(
        text="Calculate",
        command=calculate
    ).grid(column=2, row=2, sticky=W)

    root.bind('<Return>', calculate)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    feet_entry.focus()

    mainframe.columnconfigure(1, weight=1)

    root.mainloop()

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

        main_sub()

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
