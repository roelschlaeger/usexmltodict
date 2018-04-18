#!/usr/bin/env python
# -*- coding=utf-8 -*-
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

"""
Perform selected processing on .gpx files.

    SYNOPSIS

        tk6 [-h] [-v,--verbose] [--version] [ infile ]

    DESCRIPTION

        Test package for using Tkinter in place of wx

    AUTHOR

        Robert Oelschlaeger <roelsch2009@gmail.com>

    LICENSE

        This script is in the public domain.

"""

# pylint: disable=R0201
# pylint: disable=W0703

########################################################################

import sys
import os
import traceback

from tkinter import Button, Checkbutton, Entry
from tkinter import IntVar, Menu, StringVar
from tkinter import RAISED, BOTH, ACTIVE, N, E, S, W
from tkinter import Frame
from tkinter import LabelFrame
from tkinter import Text, END, NONE
from tkinter import filedialog as tkFileDialog

import make_gs
import make_rtept
from html_maps import make_html_maps

import et
import gpx2kml
import mr
import rooter

assert sys.version_info > (3, ), "Python 3 required"

########################################################################

__PROGNAME__ = "tk6.py"
__VERSION__ = "1.11.5"      # match version from sextus.py
__DATE__ = "2018-04-18"     # match date from sextus.py

########################################################################

DEFAULT_FILE_TEXT = "Filename goes here"
MIN_INDEX = 1010
DEFAULT_FLAGS = (True, False, True, False, True, True, True, True)

########################################################################

# pylint: disable=too-few-public-methods


class Options(object):
    """Dummy options class."""

    def __init__(self):
        self.html = True

########################################################################


# pylint: disable=too-many-ancestors
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
class App(Frame):
    """The main application."""

    def __init__(self, master=None, path="", flags=DEFAULT_FLAGS):
        """Initialize the frame."""
        # get the "path" keyword argument, unique to MyPanel2
        tc0_text = DEFAULT_FILE_TEXT

        if path:
            # expand to full pathname for current directory
            if not os.path.dirname(path):
                path = os.path.abspath(os.path.join(os.getcwd(), path))
            tc0_text = path

        # if no flags were passed, use the defaults
        if flags == (False,) * 8:
            flags = DEFAULT_FLAGS

        Frame.__init__(self, master, relief=RAISED)
        self.pack(fill=BOTH)
        self._create_widgets()
        self._create_menubar()
        self._initialize(tc0_text, flags)

    def about_me(self):
        """Handle About..."""
        print("about_me")

    def log(self, _s):
        """Log this string _s to the frame and the console."""
        print("%s" % _s)
        self._e2.insert(END, "\n- " + _s)
        self._e2.see(END)

    ########################################################################

    def do_et(self, pathname, et_flag, html_flag):
        """Run the ET function."""
        # self.log("do_et: %s %s %s" % (pathname, et_flag, html_flag))
        self.log("Processing ET and/or HTML")

        et_options = Options()
        et_options.html = html_flag

        body = et.do_body2(pathname, index=MIN_INDEX, options=et_options)

        if et_flag:
            output_filename = "%s.csv" % pathname
            outfile = open(output_filename, "w")
            print(body, file=outfile)
            outfile.close()
            print("et output is in %s" % output_filename)

    ########################################################################

    def do_gpx2kml(self, pathname):
        """Create a KML file from the path data."""
        self.log("Processing gpx2hkml")

        input_filename = pathname
        output_filename = None
        gpx2kml.create_kml_file(input_filename, output_filename)

    ########################################################################

    def do_mr(self, pathname):
        """Process the pathname file using mr.py."""
        self.log(f"Processing mr: {pathname}")

        mr_options = Options()
        mr.process_arg(pathname, mr_options)

    ########################################################################

    def do_rooter(self, pathname):
        """Create a Rooter HTML File."""
        self.log("Creating Rooter file")

        rooter.do_rooter(pathname)       # , options=ro_options)

    ########################################################################

    def do_rtept(self, pathname):
        """Create a Streets & Trips Route GPX File.

        Arguments:
            pathname {[type]} -- [description]
        """
        try:
            self.log("do_rtept")
            output_filename = make_rtept.do_make_rtept(pathname)
            self.log("%s created" % output_filename)
        except Exception as _e:
            print(_e)
            self.log(traceback.format_exc())

    ########################################################################

    def do_gs(self, pathname):
        """Create a Cachly gpx File.

        Arguments:
            pathname {str} -- pathname
        """
        self.log("Creating Cachly file")
        try:
            make_gs.process_arg(pathname)
        except Exception as _e:
            print(_e)
            self.log(traceback.format_exc())

    ########################################################################

    def do_html_maps(self, pathname):
        """Create a HTML Maps File.

        Arguments:
            pathname {str} -- pathname
        """
        self.log("Creating HTML Maps file")
        try:
            make_html_maps.process_arg(pathname)
        except Exception as _e:
            print(_e)
            self.log(traceback.format_exc())

    ########################################################################

    def _create_widgets(self):
        self._s1 = StringVar()
        self._s2 = StringVar()
        self._v1 = IntVar()
        self._v2 = IntVar()
        self._v3 = IntVar()
        self._v4 = IntVar()
        self._v5 = IntVar()
        self._v6 = IntVar()
        self._v7 = IntVar()
        self._v8 = IntVar()

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

        self._e2 = Text(self.lf3, height=10, width=72, wrap=NONE)
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

        self._c6 = Checkbutton(
            self.lf2,
            text="RTEPT - generate a Streets and Trips GPX _rtept file",
            variable=self._v6
        )
        self._c6.pack(anchor=W)

        self._c7 = Checkbutton(
            self.lf2,
            text="Cachly - generate a Cachly file",
            variable=self._v7
        )
        self._c7.pack(anchor=W)

        self._c8 = Checkbutton(
            self.lf2,
            text="HTML Maps - generate a HTML Maps file",
            variable=self._v8
        )
        self._c8.pack(anchor=W)

    def _create_menubar(self):
        self.menubar = Menu(self)

        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Quit", command=self.quit)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About Me", command=self.about_me)

        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

#       self.master.config(menu=self.menubar)

    def _initialize(self, tc0_text, flags):
        self._s1.set(tc0_text)
        self._s2.set("Logging")
        self._v1.set(flags[0])
        self._v2.set(flags[1])
        self._v3.set(flags[2])
        self._v4.set(flags[3])
        self._v5.set(flags[4])
        self._v6.set(flags[5])
        self._v7.set(flags[6])
        self._v8.set(flags[7])

    def b1_callback(self):
        """Handle the callback operation of the  _b1 button."""
        print(
            '"%s"' % self._e1.get(),
            self._v1.get(),
            self._v2.get(),
            self._v3.get(),
            self._v4.get(),
            self._v5.get(),
            self._v6.get(),
            self._v7.get(),
            self._v8.get(),
        )

        if self._s1.get() == DEFAULT_FILE_TEXT:
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
                "rtept_flag": self._v6.get(),
                "gs_flag": self._v7.get(),
                "hm_flag": self._v8.get(),
            }
            self.process_parameters(**_d)
            self.after_idle(self._shutdown)

    def _shutdown(self):
        """Shutdown after three seconds."""
        self.after(3000, self.quit())

    def e1_callback(self, _event):
        """Handle the callback function for _e1."""
        # print("e1_callback", "%s" % event)
        filename = tkFileDialog.askopenfilename(
            filetypes=(("gpx files", "*.gpx"), ("all files", "*.*")))
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
            rtept_flag=True,
            gs_flag=True,
            hm_flag=False
    ):
        """Perform the processing specified by pathname and flags."""
        # print(
        #     "et_flag:", et_flag, "\n",
        #     "html_flag:", html_flag, "\n",
        #     "kml_flag:", kml_flag, "\n",
        #     "mr_flag:", mr_flag, "\n",
        #     "ro_flag:", ro_flag, "\n",
        #     "rtept_flag:", rtept_flag, "\n",
        #     "gs_flag:", gs_flag, "\n",
        #     "hm_flag:", hm_flag, "\n",
        # )

        self.log("Reading from %s" % pathname)

        if not (
                et_flag or
                html_flag or
                kml_flag or
                mr_flag or
                ro_flag or
                rtept_flag or
                gs_flag or
                hm_flag
        ):
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

        if rtept_flag:
            self.log("rtept_flag: %s" % pathname)
            self.do_rtept(pathname)

        if gs_flag:
            self.do_gs(pathname)

        if hm_flag:
            self.do_html_maps(pathname)

        self.log("Done!")

########################################################################


if __name__ == "__main__":

    def main(path=None, flags=None):
        """Build the GUI and run it."""
        from tkinter import Tk

        root = Tk()
        root.title(f"Run {__PROGNAME__} .gpx processing")
        root.geometry("524x524+100+100")

        master = Frame(root)
        master.grid(column=0, row=0, sticky=(N, E, S, W))

        app = App(master, path=path, flags=flags)
        root.config(menu=app.menubar)

        for child in master.winfo_children():
            child.grid_configure(padx=5, pady=5)

        app.mainloop()

########################################################################

    HELP_DOC = f"""
    usage: {__PROGNAME__} [--help --version] [-abcdefgh] [INFILE]

    Perform selected processing on .gpx files based on Wx GUI.

        DESCRIPTION:  GUI package using Tkinter
        AUTHOR:       Robert Oelschlaeger <roelsch2009@gmail.com>

    positional arguments:
        INFILE

    optional arguments:
    --help         show this help message and exit
    --version      show program's version number and exit

    -a  enable ET - Generate Excel .csv output
    -b  enable HTML - include HTML output from et.py
    -c  enable KML - output for Google Earth
    -d  enable MR - generate a .gpx route file
    -e  enable ROOTER - generate a Rooter file
    -f  enable RTEPT - generate a Streets and Trips GPX _rtept file
    -g  enable Cachly - generate a Cachly file
    -h  enable HTML Maps - generate a HTML Maps file

    """
    from docopt import docopt

    VERSION_TEXT = f"{__PROGNAME__}  Version: {__VERSION__}  Date: {__DATE__}"

    ARGUMENTS = docopt(HELP_DOC, version=VERSION_TEXT, help=False)
    if ARGUMENTS["--help"]:
        print(HELP_DOC.strip())
        sys.exit(1)

    # print(ARGUMENTS)
    FLAGS = tuple([ARGUMENTS[f"-{x}"] for x in "abcdefgh"])
    main(path=ARGUMENTS["INFILE"], flags=FLAGS)

########################################################################
