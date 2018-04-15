#!/usr/bin/env python
# coding=utf-8

"""Apply et.py, gpx2kml.py, mr.py, rooter and make_html_maps to the same file."""

# pylint: disable=too-many-instance-attributes

# from __future__ import print_function

import sys

import wx
import et
import gpx2kml
import mr
import rooter
import make_rtept
import make_gs
from html_maps import make_html_maps

assert sys.version_info > (3, ), "Python 3 required"

########################################################################

__VERSION__ = "1.11.2"   # set cb8 default to True
__DATE__ = "2018-04-15"  #

########################################################################

DEFAULT_FILE_TEXT = "Filename goes here"
MIN_INDEX = 1010

########################################################################


# pylint: disable=too-few-public-methods
class Options(object):
    """Dummy options class."""

    def __init__(self):
        self.html = True

########################################################################


class MyPanel2(wx.Panel):
    """Display a dialog panel."""

    def __init__(self, parent, _id, *args, **kwargs):
        """Class instance initialization."""

        # get the "path" argument, unique to MyPanel2
        default_file_text = kwargs.get("path") or DEFAULT_FILE_TEXT
        del kwargs["path"]

        wx.Panel.__init__(self, parent, _id, *args, **kwargs)

        st0 = wx.StaticText(self, -1, "&Filename:")

        self.tc0 = wx.TextCtrl(
            self,
            -1,
            default_file_text,
            size=(384, -1),
            style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER
        )

        sz0 = wx.BoxSizer(wx.HORIZONTAL)
        sz0.Add(st0, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        sz0.Add(self.tc0, 0, wx.EXPAND)

        self.cb1 = wx.CheckBox(self, -1, "&ET - generate Excel .csv output")
        self.cb2 = wx.CheckBox(
            self,
            -1,
            "&HTML - include HTML output from et.py"
        )
        self.cb3 = wx.CheckBox(self, -1, "&KML - output for Google Earth")
        self.cb4 = wx.CheckBox(self, -1, "&MR - generate a .gpx route file")
        self.cb5 = wx.CheckBox(self, -1, "R&OOTER - generate a Rooter file")
        self.cb6 = wx.CheckBox(
            self,
            -1,
            "RTE&PT - generate a Streets and Trips GPX _rtept file"
        )
        self.cb7 = wx.CheckBox(
            self,
            -1,
            "&Cachly - generate a Cachly file"
        )

        self.cb8 = wx.CheckBox(
            self,
            -1,
            "H&TML Maps - generate a HTML Maps file"
        )

        button = wx.Button(self, -1, "&Run")
        self.tc1 = wx.TextCtrl(
            self,
            -1,
            "Logging\n\n",
            size=(384, 100),
            style=wx.TE_MULTILINE | wx.TE_READONLY
        )

        self.cb1.SetValue(True)
        self.cb2.SetValue(False)
        self.cb3.SetValue(True)
        self.cb4.SetValue(False)
        self.cb5.SetValue(True)
        self.cb6.SetValue(True)
        self.cb7.SetValue(True)
        self.cb8.SetValue(True)

        # set up sizers
        sb1 = wx.StaticBoxSizer(
            wx.StaticBox(
                self,
                -1,
                "Processing choices: pick at least one"
            ),
            wx.VERTICAL)
        sb1.Add(self.cb1, 0, wx.ALL, 5)
        sb1.Add(self.cb2, 0, wx.ALL, 5)
        sb1.Add(self.cb3, 0, wx.ALL, 5)
        sb1.Add(self.cb4, 0, wx.ALL, 5)
        sb1.Add(self.cb5, 0, wx.ALL, 5)
        sb1.Add(self.cb6, 0, wx.ALL, 5)
        sb1.Add(self.cb7, 0, wx.ALL, 5)
        sb1.Add(self.cb8, 0, wx.ALL, 5)

        top_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer.Add(sz0, 0, wx.CENTER | wx.ALL, 5)
        top_sizer.Add(sb1, 0, wx.CENTER | wx.ALL, 5)
        top_sizer.Add(button, 0, wx.CENTER | wx.ALL, 5)
        top_sizer.Add(self.tc1, 1, wx.EXPAND)
        self.SetSizerAndFit(top_sizer)

        self.Bind(wx.EVT_BUTTON, self.on_button, button)
        self.tc0.Bind(wx.EVT_LEFT_UP, self.on_mouse_up, self.tc0)
        self.tc0.Bind(wx.EVT_TEXT_ENTER, self.on_mouse_up, self.tc0)

    ########################################################################

    # pylint: disable=no-self-use
    def on_mouse_up(self, event):
        """Handle mouseUp event."""
        event_object = event.GetEventObject()
        current_filename = event_object.GetValue()
        if current_filename == DEFAULT_FILE_TEXT:
            current_filename = ""

        # select the file
        pathname = wx.FileSelector(
            "Select file for processing",
            default_filename=current_filename,
            default_extension=".gpx",
            wildcard="GPX (*.gpx)|*.gpx|All files (*.*)|*.*"
        )

        # if a file was specified
        if pathname != "":
            event_object.SetValue(pathname)

    ########################################################################

    def log(self, _s):
        """Log the string _s to the operator."""
        app = wx.GetApp()
        frame = app.GetTopWindow()
        frame.SetStatusText(_s)
        self.tc1.AppendText(_s + "\n")

    ########################################################################

    def on_button(self, _event):
        """Perform processing in response to the Run button."""
        # get the checkbox values
        et_flag = self.cb1.GetValue()
        html_flag = self.cb2.GetValue()
        kml_flag = self.cb3.GetValue()
        mr_flag = self.cb4.GetValue()
        ro_flag = self.cb5.GetValue()
        rtept_flag = self.cb6.GetValue()
        gs_flag = self.cb7.GetValue()
        hm_flag = self.cb8.GetValue()
        pathname = self.tc0.GetValue()

        # must have at least one checkbox selected
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
            wx.MessageBox(
                "You must select at least one of checkbox choices",
                "ERROR"
            )
            return

        if not pathname or pathname == DEFAULT_FILE_TEXT:

            # select the file
            pathname = wx.FileSelector(
                "Select file for processing",
                default_extension=".gpx",
                wildcard="GPX (*.gpx)|*.gpx|All files (*.*)|*.*"
            )

        # if a file was specified
        if pathname != "":

            self.tc0.SetValue(pathname)

            self.process_parameters(
                pathname=pathname,
                et_flag=et_flag,
                html_flag=html_flag,
                kml_flag=kml_flag,
                mr_flag=mr_flag,
                ro_flag=ro_flag,
                rtept_flag=rtept_flag,
                gs_flag=gs_flag,
                hm_flag=hm_flag
            )

            wx.Exit()

########################################################################

    # pylint: disable=too-many-arguments
    def process_parameters(
            self,
            pathname="",
            et_flag=True,
            html_flag=False,
            kml_flag=True,
            mr_flag=True,
            ro_flag=True,
            rtept_flag=False,
            gs_flag=True,
            hm_flag=False
    ):
        """Perform all processing specified by pathname and flags."""
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
        print("Done!")

########################################################################

    def do_et(self, pathname, et_flag=True, html_flag=True):
        """Create a .csv output file."""
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
        self.log("Processing mr")

        mr_options = Options()
        mr.process_arg(pathname, mr_options)

    ########################################################################

    def do_rooter(self, pathname):
        """Create a Rooter HTML File."""
        self.log("Creating Rooter file")

        rooter.do_rooter(pathname)       # , options=ro_options)

    ########################################################################

    def do_rtept(self, pathname):
        """Create a Streets & Trips Route GPX File."""
        self.log("Creating Streets & Trips GPX Route File")

        output_filename = make_rtept.do_make_rtept(pathname)
        self.log("%s created" % output_filename)

    ########################################################################

    def do_gs(self, pathname):
        """Create a Cachly gpx File."""
        self.log("Creating Cachly file")

        make_gs.process_arg(pathname)

    ########################################################################

    def do_html_maps(self, pathname):
        """Create a HTML Maps File."""
        self.log("Creating HTML Maps file")

        make_html_maps.process_arg(pathname)

########################################################################


if __name__ == '__main__':

    from argparse import ArgumentParser

    def main(path=None):
        """Process each of the command line arguments."""
        app = wx.App(redirect=False)
        app.SetAppName("quint")

        frame = wx.Frame(None, -1, "Run sextus .gpx processing")

        panel = MyPanel2(frame, -1, path=path)

        frame.CreateStatusBar()
        frame.GetStatusBar().SetStatusText("Ready!")

        top_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer.Add(panel, 1, wx.EXPAND)
        frame.SetSizerAndFit(top_sizer)

        frame.CenterOnScreen()

        frame.Show()
        app.MainLoop()

    ########################################################################

    PARSER = ArgumentParser(
        description=__doc__
    )

    PARSER.add_argument(
        "infile",
        nargs="?",
        type=str
    )

    PARSER.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="count",
        help="increment debug counter"
    )

    PARSER.add_argument(
        "-v",
        "--version",
        action="version",
        version="%%(prog)s, Version: %s %s" % (__VERSION__, __DATE__)
    )

    NAMESPACE = PARSER.parse_args()

    main(path=NAMESPACE.infile)

########################################################################
