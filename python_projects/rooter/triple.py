#!/usr/bin/python
# vim:ts=4:sw=4:tw=0:wm=0:et

########################################################################

"""Apply et.py, gpx2kml.py and mr.py to the same file"""

########################################################################

import sys

import wx

import et
import gpx2kml
import mr

assert sys.version_info > (3, ), "Python 3 required"

__VERSION__ = "0.0.3"
__DATE__ = "2017-07-28"

########################################################################

DEFAULT_FILE_TEXT = "Filename goes here"
MIN_INDEX = 1010

########################################################################


class Options(object):
    """Dummy options class"""

    html = False

########################################################################


class MyPanel2(wx.Panel):
    """Display panel for dialog."""

    def __init__(self, parent, _id, *args, **kwargs):

        wx.Panel.__init__(self, parent, _id, *args, **kwargs)

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

        self.cb2 = wx.CheckBox(
            self,
            -1,
            "&HTML - include HTML output from et.py"
        )
        self.cb3 = wx.CheckBox(self, -1, "&KML - output for Google Earth")

        button = wx.Button(self, -1, "&Run")
        self.tc1 = wx.TextCtrl(
            self,
            -1,
            "Logging\n\n",
            size=(384, 100),
            style=wx.TE_MULTILINE | wx.TE_READONLY
        )

        self.cb2.SetValue(True)
        self.cb3.SetValue(True)

        # set up sizers
        sb1 = wx.StaticBoxSizer(
            wx.StaticBox(
                self,
                -1,
                "Processing choices: pick at least one"
            ),
            wx.VERTICAL)
        sb1.Add(self.cb2, 0, wx.ALL, 5)
        sb1.Add(self.cb3, 0, wx.ALL, 5)

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

    def on_mouse_up(self, event):
        """Event handler for mouse up event."""

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
        """Log the L{_s} string to the status window."""

        app = wx.GetApp()
        frame = app.GetTopWindow()
        frame.SetStatusText(_s)
        self.tc1.AppendText(_s + "\n")

    ########################################################################

    def on_button(self, _event):
        """Handle the button event."""

        # get the checkbox values
        html = self.cb2.GetValue()
        kml = self.cb3.GetValue()

        # must have at least one checkbox selected
        if not (html or kml):
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
            if html:
                self.do_et(pathname, html_flag=html)

            if kml:
                self.do_gpx2kml(pathname)

            self.log("Done!")

    ########################################################################

    def do_et(self, pathname, html_flag=True):
        """Handle processing for ET checkbox."""

        self.log("Processing ET and/or HTML")

        et_options = Options()
        et_options.html = html_flag

        et.do_body2(pathname, index=MIN_INDEX, options=et_options)

    ########################################################################

    def do_gpx2kml(self, pathname):
        """Handle processing for KML checkbox."""

        self.log("Processing gpx2hkml")

        input_filename = pathname
        output_filename = None
        gpx2kml.create_kml_file(input_filename, output_filename)

    ########################################################################

    def do_mr(self, pathname):
        """Handle processing for MR checkbox."""

        self.log("Processing mr")

        mr_options = Options()
        mr.process_arg(pathname, mr_options)

########################################################################


def main(_options):
    """process each of the command line arguments"""

    app = wx.App(redirect=False)
    app.SetAppName("triple")

    frame = wx.Frame(None, -1, "Run triple .gpx processing")

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


if __name__ == '__main__':

    from argparse import ArgumentParser

    PARSER = ArgumentParser()

    PARSER.add_argument(
        "-v",
        "--version",
        action="version",
        version="%%(prog)s: Version: %s %s" % (__VERSION__, __DATE__)
    )

    PARSER.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="count",
        help="increment debug counter")

    main(PARSER.parse_args())

########################################################################
