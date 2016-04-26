#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 19 Mar 2014 02:16:55 PM CDT
# Last Modified: Mon 15 Feb 2016 10:18:52 PM CST

from __future__ import print_function

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

import sys

if sys.version_info < (3,):
    from Tix import Button, Checkbutton, Entry
#   from Tix import Frame
    from Tix import IntVar, Menu, StringVar

    from Tkconstants import RAISED, BOTH, ACTIVE, N, E, S, W

    from ttk import Frame
    from ttk import LabelFrame

    import tkFileDialog

else:
    from tkinter.tix import Button, Checkbutton, Entry
#   from tkinter.tix import Frame
    from tkinter.tix import IntVar, Menu, StringVar

    from tkinter.constants import RAISED, BOTH, ACTIVE, N, E, S, W

    from tkinter.ttk import Frame
    from tkinter.ttk import LabelFrame

    from tkinter import filedialog as tkFileDialog

########################################################################


class App(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master, relief=RAISED)
        self.pack(fill=BOTH)
        self.CreateWidgets()
        self.CreateMenubar()
        self.Initialize()

    def aboutMe(self):
        print("aboutMe")

    def log(self, s):
        # DEBUG
        print("%s" % s)

    def do_et(self, pathname, et_flag, html_flag):
        print("do_et")
        pass

    def do_gpx2kml(self, pathname):
        print("do_gpx2kml")
        pass

    def do_mr(self, pathname):
        print("do_mr")
        pass

    def do_rooter(self, pathname):
        print("do_rooter")
        pass

    def CreateWidgets(self):
        self.s1 = StringVar()
        self.s2 = StringVar()
        self.v1 = IntVar()
        self.v2 = IntVar()
        self.v3 = IntVar()
        self.v4 = IntVar()
        self.v5 = IntVar()

        self.lf1 = LabelFrame(self, text="Filename:")
        self.lf1.pack(fill=BOTH)

        self.lf2 = LabelFrame(
            self,
            text="Processing choices: pick at least one"
        )
#       self.lf2.config(label="Processing choices: pick at least one")
        self.lf2.pack(fill=BOTH)

        self.lf3 = LabelFrame(self, text="Logging")
#       self.lf3.config(label="Logging")
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
        self.filemenu.add_command(label="Quit", command=self.quit)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About Me", command=self.aboutMe)

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

#       self.master.config(menu=self.menubar)

    def Initialize(self):
        self.s1.set("Filename goes here")
        self.s2.set("Logging")
        self.v1.set(1)
        self.v2.set(0)
        self.v3.set(1)
        self.v4.set(1)
        self.v5.set(1)

    def b1_callback(self):
        print('"%s"' % self.e1.get(),
              self.v1.get(),
              self.v2.get(),
              self.v3.get(),
              self.v4.get(),
              self.v5.get()
              )

        if self.s1.get() == "Filename goes here":
            self.e1_callback(None)
            return
        else:
            print("Process %s" % self.s1.get())
            d = {
                "pathname": self.s1.get(),
                "et_flag": self.v1.get(),
                "html_flag": self.v2.get(),
                "kml_flag": self.v3.get(),
                "mr_flag": self.v4.get(),
                "ro_flag": self.v5.get(),
            }
            self.process_parameters(**d)

    def e1_callback(self, event):
        print("e1_callback", "%s" % event)
        filename = tkFileDialog.askopenfilename()
        if filename:
            self.s1.set(filename)

    ########################################################################

    def process_parameters(
        self,
        pathname="",
        et_flag=True,
        html_flag=False,
        kml_flag=True,
        mr_flag=True,
        ro_flag=True,
    ):
        """Perform the processing specified by pathname and flags"""

        # DEBUG
        print(
            "et_flag:", et_flag, "\n",
            "html_flag:", html_flag, "\n",
            "kml_flag:", kml_flag, "\n",
            "mr_flag:", mr_flag, "\n",
            "ro_flag:", ro_flag, "\n",
        )

        self.log("Reading from %s" % pathname)

        if not (et_flag or html_flag or kml_flag or mr_flag or ro_flag):
            self.log("ERROR: Nothing to do: no flags set")
            return

        # perform the processing
        if (et_flag or html_flag):
            self.do_et(pathname, et_flag=et_flag, html_flag=html_flag)

        if kml_flag:
            self.do_gpx2kml(pathname)

        if mr_flag:
            self.do_mr(pathname)

        if ro_flag:
            self.do_rooter(pathname)

        self.log("Done!")

        self.destroy()


########################################################################

if __name__ == "__main__":

    if sys.version_info < (3,):
        from Tix import Tk
    else:
        from tkinter.tix import Tk

    root = Tk()
    root.title("Run quint .gpx processing")
    root.geometry("450x300+200+200")
#   root.minsize(400, 200)

    master = Frame(root, padding=(3, 3, 12, 12))
    master.grid(column=0, row=0, sticky=(
        N,
        E,
        S,
        W)
    )

    app = App(master)
    root.config(menu=app.menubar)

    for child in master.winfo_children():
        child.grid_configure(padx=5, pady=5)

    app.mainloop()

########################################################################
