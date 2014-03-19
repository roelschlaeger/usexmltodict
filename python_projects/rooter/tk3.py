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

__VERSION__ = "0.0.1"

########################################################################

from Tkinter import ACTIVE, Button, Checkbutton, Entry, IntVar, LabelFrame, Tk
from Tkinter import StringVar, W

########################################################################

root = Tk()

# frame = Frame(root, height=128, width=128)
frame = root

v1 = IntVar()
v2 = IntVar()
v3 = IntVar()
v4 = IntVar()
v5 = IntVar()
s1 = StringVar()
s1.set("filename goes here")

v1.set(1)
v2.set(0)
v3.set(1)
v4.set(1)
v5.set(1)

lf1 = LabelFrame(frame, text="File:", padx=5, pady=5)
e1 = Entry(lf1, textvariable=s1)

lf2 = LabelFrame(frame, text="Switches", padx=5, pady=5)
c1 = Checkbutton(lf2, text="ET - generate Excel .csv output", variable=v1)
c2 = Checkbutton(
    lf2,
    text="HTML - include HTML output from et.py",
    variable=v2
)
c3 = Checkbutton(lf2, text="KML - output for Google Earth", variable=v3)
c4 = Checkbutton(lf2, text="MR - generate a .gpx route file", variable=v4)
c5 = Checkbutton(lf2, text="ROOTER - generate a Rooter file", variable=v5)


def b1_callback():
    print '"%s"' % e1.get(), v1.get(), v2.get(), v3.get(), v4.get(), v5.get()

b1 = Button(frame, text="Run", command=b1_callback, default=ACTIVE, activebackground="#f00")

e1.pack()
lf1.pack()

lf2.pack()
c1.pack(anchor=W)
c2.pack(anchor=W)
c3.pack(anchor=W)
c4.pack(anchor=W)
c5.pack(anchor=W)

b1.pack()

root.mainloop()

########################################################################
