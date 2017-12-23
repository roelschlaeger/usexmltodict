#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Wed 19 Mar 2014 02:16:55 PM CDT
# Last Modified: Tue 02 Jun 2015 10:26:21 AM CDT

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

########################################################################


# pylint: disable=multiple-statements
import sys; assert sys.version_info > (3, ), "Python 3 required"  # noqa: E702

from tkinter import ACTIVE, BOTH, IntVar, Menu, RAISED, StringVar, W
from tkinter import Button, Checkbutton, Entry, Frame, LabelFrame

########################################################################

__VERSION__ = "0.0.2"
__DATE__ = "2017-07-28"

########################################################################


# pylint: disable=too-many-ancestors,too-many-instance-attributes,no-self-use
class App(Frame):
    """The main Tk app."""

    def __init__(self, master=None):
        Frame.__init__(self, master, relief=RAISED)
        self.pack(fill=BOTH)
        self.create_widgets()
        self.create_menubar()
        self.initialize()

    def about_me(self):
        """Handle About event."""
        print("about_me")

    def create_widgets(self):
        """Create class widgets."""
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
        self.lf2.pack(fill=BOTH)

        self.lf3 = LabelFrame(self, text="Logging")
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

    def create_menubar(self):
        """Create the application menubar."""
        self.menubar = Menu(self)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Quit", command=self.quit)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About Me", command=self.about_me)

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.master.config(menu=self.menubar)

    def initialize(self):
        """Perform all initialization."""
        self._s1.set("Filename goes here")
        self._s2.set("Logging")
        self._v1.set(1)
        self._v2.set(0)
        self._v3.set(1)
        self._v4.set(1)
        self._v5.set(1)

    def b1_callback(self):
        """Callback function for button1."""
        print('"%s"' % self._e1.get(), self._v1.get(), self._v2.get(),
              self._v3.get(), self._v4.get(), self._v5.get())

    def e1_callback(self, event):
        """Callback function for entry1."""
        print("e1_callback", "%s" % event)
        from tkinter import filedialog
        filename = filedialog.askopenfilename()
        del filename  # just discard to keep Lint happy

########################################################################


if __name__ == "__main__":

    def main():
        """Main program for testing."""

        app = App()

        app.master.title("Run quint .gpx processing")
        app.master.geometry("450x300+200+200")

        app.mainloop()

########################################################################

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

    PARSER.parse_args()

    main()

########################################################################
