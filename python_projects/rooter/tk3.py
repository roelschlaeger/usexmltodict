#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 19 Mar 2014 02:16:55 PM CDT
# Last Modified: Wed 19 Mar 2014 03:57:07 PM CDT

"""
SYNOPSIS

    tk3 [-h] [-v,--verbose] [--version]

DESCRIPTION

    Test package for using Tkinter in place of wx

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

########################################################################

from __future__ import print_function

# pylint: disable=C0321
import sys; assert sys.version_info > (3, ), "Python 3 required"  # noqa: E303, E702

from tkinter import ACTIVE, Button, Checkbutton, Entry, IntVar, LabelFrame, Tk
from tkinter import StringVar, W

########################################################################

__VERSION__ = "0.0.2"
__DATE__ = "2017-07-27"

########################################################################


# pylint: disable=too-many-locals
def main(_args):
    """Dummy mainline routein for testing use of Tk in lieu of Wx."""

    root = Tk()

    # frame = Frame(root, height=128, width=128)
    frame = root

    _v1 = IntVar()
    _v2 = IntVar()
    _v3 = IntVar()
    _v4 = IntVar()
    _v5 = IntVar()
    _s1 = StringVar()
    _s1.set("filename goes here")

    _v1.set(1)
    _v2.set(0)
    _v3.set(1)
    _v4.set(1)
    _v5.set(1)

    lf1 = LabelFrame(frame, text="File:", padx=5, pady=5)
    _e1 = Entry(lf1, textvariable=_s1)

    lf2 = LabelFrame(frame, text="Switches", padx=5, pady=5)
    _c1 = Checkbutton(lf2, text="ET - generate Excel .csv output", variable=_v1)  # noqa: E501
    _c2 = Checkbutton(
        lf2,
        text="HTML - include HTML output from et.py",
        variable=_v2
    )
    _c3 = Checkbutton(lf2, text="KML - output for Google Earth", variable=_v3)
    _c4 = Checkbutton(lf2, text="MR - generate a .gpx route file", variable=_v4)  # noqa: E501
    _c5 = Checkbutton(lf2, text="ROOTER - generate a Rooter file", variable=_v5)  # noqa: E501

    def b1_callback():
        """Button 1 callback handler."""
        print(
            '"%s"' % _e1.get(),
            _v1.get(),
            _v2.get(),
            _v3.get(),
            _v4.get(),
            _v5.get()
            )

    _b1 = Button(
        frame,
        text="Run",
        command=b1_callback,
        default=ACTIVE,
        activebackground="#f00"
        )

    _e1.pack()
    lf1.pack()

    lf2.pack()
    _c1.pack(anchor=W)
    _c2.pack(anchor=W)
    _c3.pack(anchor=W)
    _c4.pack(anchor=W)
    _c5.pack(anchor=W)

    _b1.pack()

    root.mainloop()

########################################################################


if __name__ == '__main__':

    from argparse import ArgumentParser

    PARSER = ArgumentParser()

    PARSER.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="count",
        help="increment debug counter")

    PARSER.add_argument(
        "--version",
        action="version",
        version="%%(prog)s, Version: %s %s" % (__VERSION__, __DATE__)
        )

    main(PARSER.parse_args())

########################################################################

# end of file
