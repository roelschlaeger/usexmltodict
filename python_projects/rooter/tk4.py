#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 19 Mar 2014 02:16:55 PM CDT
# Last Modified: Thu 20 Mar 2014 02:55:52 PM CDT

"""
SYNOPSIS

    tk4 [-h] [-v,--verbose] [--version]

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

from Tkinter import ACTIVE, BOTH, Button, Checkbutton, Entry, Frame, IntVar
from Tkinter import LabelFrame, RAISED, StringVar, W

########################################################################


class App(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master, relief=RAISED)
        self.pack(fill=BOTH)
        self.CreateWidgets()
        self.Initialize()

    def CreateWidgets(self):
        self.s1 = StringVar()
        self.s2 = StringVar()
        self.v1 = IntVar()
        self.v2 = IntVar()
        self.v3 = IntVar()
        self.v4 = IntVar()
        self.v5 = IntVar()

        self.lf1 = LabelFrame(self, text="Filename:", padx=5, pady=5)
        self.lf1.pack(fill=BOTH)

        self.lf2 = LabelFrame(
            self,
            text="Processing choices: pick at least one",
            padx=5,
            pady=5
        )
        self.lf2.pack(fill=BOTH)

        self.lf3 = LabelFrame(self, text="Logging", padx=5, pady=5)
        self.lf3.pack(fill=BOTH)

        self.b1 = Button(
            self,
            text="Run",
            command=self.b1_callback,
            default=ACTIVE,
            activebackground="#f00"
        )
        self.b1.pack()

        self.e1 = Entry(
            self.lf1,
#           command=self.e1_callback,
            textvariable=self.s1
        )
        self.e1.pack(fill=BOTH)

        self.e2 = Entry(self.lf3, textvariable=self.s2)
        self.e2.pack(fill=BOTH)

        self.c1 = Checkbutton(
            self.lf2,
            text="ET - generate Excel .csv output",
            variable=self.v1
        )
        self.c1.pack(anchor=W)

        self.c2 = Checkbutton(
            self.lf2,
            text="HTML - include HTML output from et.py",
            variable=self.v2
        )
        self.c2.pack(anchor=W)

        self.c3 = Checkbutton(
            self.lf2,
            text="KML - output for Google Earth",
            variable=self.v3
        )
        self.c3.pack(anchor=W)

        self.c4 = Checkbutton(
            self.lf2,
            text="MR - generate a .gpx route file",
            variable=self.v4
        )
        self.c4.pack(anchor=W)

        self.c5 = Checkbutton(
            self.lf2,
            text="ROOTER - generate a Rooter file",
            variable=self.v5
        )
        self.c5.pack(anchor=W)

    def Initialize(self):
        self.s1.set("Filename goes here")
        self.s2.set("Logging")
        self.v1.set(1)
        self.v2.set(0)
        self.v3.set(1)
        self.v4.set(1)
        self.v5.set(1)

    def b1_callback(self):
        print '"%s"' % self.e1.get(), \
            self.v1.get(), \
            self.v2.get(), \
            self.v3.get(), \
            self.v4.get(), \
            self.v5.get()

    def e1_callback(self):
        print "e1_callback"

    ########################################################################

if __name__ == "__main__":

    app = App()

    app.master.title("Run quint .gpx processing")
#   app.master.maxsize(1000, 400)
    app.master.geometry("450x300+200+200")

    app.mainloop()

########################################################################
