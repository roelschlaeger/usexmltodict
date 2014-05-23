#!/usr/bin/python
# vim:ts=4:sw=4:tw=0:wm=0:et
# $Id: $
# Created: 	     Fri 31 Dec 2010 05:38:29 PM CST
# Last modified: Fri 23 May 2014 11:18:29 AM CDT

########################################################################

"""Apply et.py, gpx2kml.py and mr.py to the same file"""

__version__ = "$Revision: $".split()[1]
__date__ = "$Date: $".split()[1]

########################################################################

DEFAULT_FILE_TEXT = "Filename goes here"
MIN_INDEX = 1010

########################################################################

import wx

import et
import gpx2kml
import mr
import rooter

########################################################################


class Options(object):
    """Dummy options class"""
    pass

########################################################################


class MyPanel2(wx.Panel):

    def __init__(self, parent, id, *args, **kwargs):

        wx.Panel.__init__(self, parent, id, *args, **kwargs)

        st0 = wx.StaticText(self, -1, "&Filename:")
        self.tc0 = wx.TextCtrl(
            self,
            -1,
            DEFAULT_FILE_TEXT,
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
        self.cb5 = wx.CheckBox(self, -1, "&ROOTER - generate a Rooter file")

        button = wx.Button(self,   -1, "&Run")
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
        self.cb4.SetValue(True)
        self.cb5.SetValue(True)

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

        top_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer.Add(sz0,      0, wx.CENTER | wx.ALL, 5)
        top_sizer.Add(sb1,      0, wx.CENTER | wx.ALL, 5)
        top_sizer.Add(button,   0, wx.CENTER | wx.ALL, 5)
        top_sizer.Add(self.tc1, 1, wx.EXPAND)
        self.SetSizerAndFit(top_sizer)

        self.Bind(wx.EVT_BUTTON,         self.on_button,   button)
        self.tc0.Bind(wx.EVT_LEFT_UP,    self.on_mouse_up, self.tc0)
        self.tc0.Bind(wx.EVT_TEXT_ENTER, self.on_mouse_up, self.tc0)

    ########################################################################

    def on_mouse_up(self, event):

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

    def log(self, s):

        app = wx.GetApp()
        frame = app.GetTopWindow()
        frame.SetStatusText(s)
        self.tc1.AppendText(s + "\n")

    ########################################################################

    def on_button(self, event):
        """Perform processing in response to the Run button"""

        # get the checkbox values
        et_flag = self.cb1.GetValue()
        html_flag = self.cb2.GetValue()
        kml_flag = self.cb3.GetValue()
        mr_flag = self.cb4.GetValue()
        ro_flag = self.cb5.GetValue()

        # must have at least one checkbox selected
        if not (et_flag or html_flag or kml_flag or mr_flag or ro_flag):
            wx.MessageBox(
                "You must select at least one of checkbox choices",
                "ERROR"
            )
            return

        pathname = self.tc0.GetValue()
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

            self.log("Reading from %s" % pathname)

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

    ########################################################################

    def do_et(self, pathname, et_flag=True, html_flag=True):

        self.log("Processing ET and/or HTML")

        et_options = Options()
        et_options.html = html_flag

        # TODO use UserSort for Index
        body = et.do_body2(pathname, index=MIN_INDEX, options=et_options)

        if et_flag:
            output_filename = "%s.csv" % pathname
            outfile = open(output_filename, "w")
            print >>outfile, body
            outfile.close()
            print "et output is in %s" % output_filename

    ########################################################################

    def do_gpx2kml(self, pathname):
        """Create a KML file from the path data"""

        self.log("Processing gpx2hkml")

        input_filename = pathname
        output_filename = None
        gpx2kml.create_kml_file(input_filename, output_filename)

    ########################################################################

    def do_mr(self, pathname):

        self.log("Processing mr")

        mr_options = Options()
        mr.process_arg(pathname, mr_options)

    ########################################################################

    def do_rooter(self, pathname):

        self.log("Creating Rooter file")

        rooter.do_rooter(pathname)       # , options=ro_options)

########################################################################


def main(args, options):
    """process each of the command line arguments"""

    app = wx.App(redirect=False)
    app.SetAppName("quint")

### config = wx.FileConfig(localFilename="options")
### config.Create()
### print "config.GetPath()=%s" % config.GetPath()

    frame = wx.Frame(None, -1, "Run quint .gpx processing")

    panel = MyPanel2(frame, -1)

    frame.CreateStatusBar()
    frame.GetStatusBar().SetStatusText("Ready!")

    top_sizer = wx.BoxSizer(wx.VERTICAL)
    top_sizer.Add(panel, 1, wx.EXPAND)
    frame.SetSizerAndFit(top_sizer)

    frame.CenterOnScreen()

    frame.Show()
    app.MainLoop()

########################################################################

from optparse import OptionParser
import sys

USAGE = "%prog { options }"
VERSION = "Version: %(version)s, %(date)s" % {
    "version":   __version__,
    "date":   __date__,
}

PARSER = OptionParser(usage=USAGE, version=VERSION)

PARSER.add_option(
    "-d",
    "--debug",
    dest="debug",
    action="count",
    help="increment debug counter"
)

(OPTIONS, ARGS) = PARSER.parse_args()

if ARGS:
    PARSER.print_help()
    sys.exit(1)

main(ARGS, OPTIONS)

########################################################################
