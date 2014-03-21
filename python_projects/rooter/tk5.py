#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 19 Mar 2014 02:16:55 PM CDT
# Last Modified: Fri 21 Mar 2014 03:30:24 PM CDT

"""
SYNOPSIS

    tk5 [-h] [-v,--verbose] [--version]

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

__VERSION__ = "0.0.2"

########################################################################

# import Tix
# from Tix import ACTIVE, BOTH, Button, Checkbutton, Entry, Frame, IntVar
# from Tix import LabelFrame, Menu, RAISED, StringVar, W
# from Tkconstants import *
# from Tkinter import ACTIVE, BOTH, IntVar, Menu, RAISED, StringVar, W
# from ttk import Button, Checkbutton, Entry, Frame, LabelFrame

from Tix import *
from Tkconstants import *
import tkFileDialog

#   import tkFileDialog as filedialog
#   from pprint import pprint
#   dirname = tkFileDialog.askdirectory()
#   pprint(dirname)
#   filename = tkFileDialog.askopenfile()
#   pprint(filename)
#   filename = tkFileDialog.askopenfilename()
#   pprint(filename)
#   filename = tkFileDialog.askopenfilenames()
#   pprint(filename)
#   filename = tkFileDialog.askopenfiles()
#   pprint(filename)
#   filename = tkFileDialog.asksaveasfile()
#   pprint(filename)
#   filename = tkFileDialog.asksaveasfilename()
#   pprint(filename)

########################################################################


class App(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master, relief=RAISED)
        self.pack(fill=BOTH)
        self.CreateWidgets()
        self.CreateMenubar()
        self.Initialize()

    def aboutMe(self):
        print "aboutMe"

    def CreateWidgets(self):
        self.s1 = StringVar()
        self.s2 = StringVar()
        self.v1 = IntVar()
        self.v2 = IntVar()
        self.v3 = IntVar()
        self.v4 = IntVar()
        self.v5 = IntVar()

#       self.lf1 = LabelFrame(self, text="Filename:")
        self.lf1 = Frame(self)
        self.lf1.pack(fill=BOTH)

#       self.lf2 = LabelFrame(self, text="Processing choices: pick at least one")
        self.lf2 = Frame(self)
        self.lf2.pack(fill=BOTH)

        self.lf3 = Frame(self)
#       self.lf3 = LabelFrame(self, text="Logging")
        self.lf3.pack(fill=BOTH)

        self.b1 = Button(
            self,
            text="Run",
            command=self.b1_callback,
            default=ACTIVE
        )
        self.b1.pack(side="bottom")

        self.e1 = Entry(
            self.lf1,
            textvariable=self.s1
        )
        self.e1.pack(fill=BOTH)
        self.e1.bind("<Button-1>", self.e1_callback)

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

    def CreateMenubar(self):
        self.menubar = Menu(self)

        self.filemenu = Menu(self.menubar, tearoff=0)
#       self.filemenu.add_separator()
        self.filemenu.add_command(label="Quit", command=self.quit)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About Me", command=self.aboutMe)

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.master.config(menu=self.menubar)

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

        if self.s1.get() == "Filename goes here":
            self.e1_callback(None)
            return
        else:
            print "Process %s" % self.s1.get()

    def e1_callback(self, event):
        print "e1_callback", "%s" % event
        filename = tkFileDialog.askopenfilename()
        if filename:
            self.s1.set(filename)

    ########################################################################

    ########################################################################

if __name__ == "__main__":

    app = App()

    app.master.title("Run quint .gpx processing")
#   app.master.maxsize(1000, 400)
    app.master.geometry("450x300+200+200")

    app.mainloop()

########################################################################
