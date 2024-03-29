#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

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

from __future__ import print_function

# pylint: disable=R0201

########################################################################

import sys

from tkinter import Button, Checkbutton, Entry
from tkinter import IntVar, Menu, StringVar
from tkinter import RAISED, BOTH, ACTIVE, N, E, S, W
from tkinter import Frame
from tkinter import LabelFrame
from tkinter import filedialog as tkFileDialog

assert sys.version_info > (3, ), "Python 3 required"

########################################################################

__VERSION__ = "0.0.3"
__DATE__ = "2017-07-28"

########################################################################


# pylint: disable=too-many-ancestors
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
class App(Frame):
    """The main application."""

    def __init__(self, master=None):
        Frame.__init__(self, master, relief=RAISED)
        self.pack(fill=BOTH)
        self._create_widgets()
        self._create_menubar()
        self._initialize()

    def about_me(self):
        """Handle About..."""
        print("about_me")

    def log(self, _s):
        """Dummy log function."""
        print("%s" % _s)

    def do_et(self, pathname, et_flag, html_flag):
        """Dummy function for ET."""
        print("do_et", pathname, et_flag, html_flag)

    def do_gpx2kml(self, _pathname):
        """Dummy function for GPX2KML."""
        print("do_gpx2kml")

    def do_mr(self, pathname):
        """Dummy function for MR."""
        print("do_mr", pathname)

    def do_rooter(self, pathname):
        """Dummy function for ROOTER."""
        print("do_rooter", pathname)

    def _create_widgets(self):
        self._s1 = StringVar()
        self._s2 = StringVar()
        self._v1 = IntVar()
        self._v2 = IntVar()
        self._v3 = IntVar()
        self._v4 = IntVar()
        self._v5 = IntVar()

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

        self._b1 = Button(
            self,
            text="Run",
            command=self.b1_callback,
            default=ACTIVE
        )
        self._b1.pack(side="bottom")

        self._e1 = Entry(
            self.lf1,
            textvariable=self._s1
        )
        self._e1.pack(fill=BOTH)
        self._e1.bind("<Button-1>", self.e1_callback)

        self._e2 = Entry(self.lf3, textvariable=self._s2)
        self._e2.pack(fill=BOTH)

        self._c1 = Checkbutton(
            self.lf2,
            text="ET - generate Excel .csv output",
            variable=self._v1
        )
        self._c1.pack(anchor=W)

        self._c2 = Checkbutton(
            self.lf2,
            text="HTML - include HTML output from et.py",
            variable=self._v2
        )
        self._c2.pack(anchor=W)

        self._c3 = Checkbutton(
            self.lf2,
            text="KML - output for Google Earth",
            variable=self._v3
        )
        self._c3.pack(anchor=W)

        self._c4 = Checkbutton(
            self.lf2,
            text="MR - generate a .gpx route file",
            variable=self._v4
        )
        self._c4.pack(anchor=W)

        self._c5 = Checkbutton(
            self.lf2,
            text="ROOTER - generate a Rooter file",
            variable=self._v5
        )
        self._c5.pack(anchor=W)

    def _create_menubar(self):
        self.menubar = Menu(self)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Quit", command=self.quit)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About Me", command=self.about_me)

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

#       self.master.config(menu=self.menubar)

    def _initialize(self):
        self._s1.set("Filename goes here")
        self._s2.set("Logging")
        self._v1.set(1)
        self._v2.set(0)
        self._v3.set(1)
        self._v4.set(1)
        self._v5.set(1)

    def b1_callback(self):
        """Callback function for _b1."""
        print(
            '"%s"' % self._e1.get(),
            self._v1.get(),
            self._v2.get(),
            self._v3.get(),
            self._v4.get(),
            self._v5.get()
            )

        if self._s1.get() == "Filename goes here":
            self.e1_callback(None)
            return
        else:
            print("Process %s" % self._s1.get())
            _d = {
                "pathname": self._s1.get(),
                "et_flag": self._v1.get(),
                "html_flag": self._v2.get(),
                "kml_flag": self._v3.get(),
                "mr_flag": self._v4.get(),
                "ro_flag": self._v5.get(),
            }
            self.process_parameters(**_d)

    def e1_callback(self, event):
        """Callback function for _e1."""
        print("e1_callback", "%s" % event)
        filename = tkFileDialog.askopenfilename()
        if filename:
            self._s1.set(filename)

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
        if et_flag or html_flag:
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

    def main():
        """Main function."""

        from tkinter import Tk

        root = Tk()
        root.title("Run quint .gpx processing")
        root.geometry("450x300+200+200")
    #   root.minsize(400, 200)

        # master = Frame(root, padding=(3, 3, 12, 12))
        master = Frame(root)
        master.grid(column=0, row=0, sticky=(N, E, S, W))

        app = App(master)
        root.config(menu=app.menubar)

        for child in master.winfo_children():
            child.grid_configure(padx=5, pady=5)

        app.mainloop()

########################################################################

    from argparse import ArgumentParser

    PARSER = ArgumentParser(
        description=__doc__
    )

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

    PARSER.parse_args()

    main()

########################################################################
