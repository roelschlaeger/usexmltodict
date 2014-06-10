#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Tue 10 Jun 2014 12:39:08 PM CDT
# Last Modified: Tue 10 Jun 2014 04:48:56 PM CDT

"""
SYNOPSIS

    TODO helloworld [-h] [-v,--verbose] [--version]

DESCRIPTION

    TODO This describes how to use this script.
    This docstring will be printed by the script if there is an error or
    if the user requests help (-h or --help).

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

from gpxpy.gpx import GPXWaypoint

WPT_EXTENSIONS = """
    <gsak:wptExtension xmlns:gsak="http://www.gsak.net/xmlv1/6">
      <gsak:UserFlag>%(UserFlag)s</gsak:UserFlag>
      <gsak:Lock>%(Lock)s</gsak:Lock>
      <gsak:DNF>%(DNF)s</gsak:DNF>
      <gsak:Watch>%(Watch)s</gsak:Watch>
      <gsak:UserData>%(UserData)s</gsak:UserData>
      <gsak:FirstToFind>%(FirstToFind)s</gsak:FirstToFind>
      <gsak:User2>%(User2)s</gsak:User2>
      <gsak:User3>%(User3)s</gsak:User3>
      <gsak:User4>%(User4)s</gsak:User4>
      <gsak:County>%(County)s</gsak:County>
      <gsak:UserSort>%(UserSort)d</gsak:UserSort>
      <gsak:SmartName>%(SmartName)s</gsak:SmartName>
      <gsak:LastGpxDate>%(LastGpxDate)s</gsak:LastGpxDate>
      <gsak:Code>%(Code)s</gsak:Code>
      <gsak:Resolution>%(Resolution)s</gsak:Resolution>
      <gsak:IsPremium>%(IsPremium)s</gsak:IsPremium>
      <gsak:FavPoints>%(FavPoints)d</gsak:FavPoints>
      <gsak:GcNote>%(GcNote)s</gsak:GcNote>
      <gsak:Guid>%(Guid)s</gsak:Guid>
      <gsak:CacheImages>%(CacheImages)s</gsak:CacheImages>
      <gsak:LogImages>%(LogImages)s</gsak:LogImages>
      <gsak:CustomData>%(CustomData)s</gsak:CustomData>
    </gsak:wptExtension>
"""

EXTENSIONS = """
  <extensions>
    <groundspeak:cache id="3657994" available="True" archived="False" xmlns:groundspeak="http://www.groundspeak.com/cache/1/0/1">
      <groundspeak:name>FINAL Walking Dead - Rock Out</groundspeak:name>
      <groundspeak:placed_by>Razor1965</groundspeak:placed_by>
      <groundspeak:owner id="597121">Razor1965</groundspeak:owner>
      <groundspeak:type>Unknown Cache</groundspeak:type>
      <groundspeak:container>Micro</groundspeak:container>
      <groundspeak:attributes>
        <groundspeak:attribute id="7" inc="1">Takes less than an hour</groundspeak:attribute>
        <groundspeak:attribute id="13" inc="0">Available at all times</groundspeak:attribute>
        <groundspeak:attribute id="19" inc="1">Ticks</groundspeak:attribute>
        <groundspeak:attribute id="25" inc="1">Parking available</groundspeak:attribute>
        <groundspeak:attribute id="30" inc="1">Picnic tables nearby</groundspeak:attribute>
        <groundspeak:attribute id="32" inc="1">Bicycles</groundspeak:attribute>
        <groundspeak:attribute id="37" inc="1">Horses</groundspeak:attribute>
        <groundspeak:attribute id="40" inc="1">Stealth required</groundspeak:attribute>
        <groundspeak:attribute id="53" inc="1">Park and Grab</groundspeak:attribute>
      </groundspeak:attributes>
      <groundspeak:difficulty></groundspeak:difficulty>
      <groundspeak:terrain></groundspeak:terrain>
      <groundspeak:country></groundspeak:country>
      <groundspeak:state></groundspeak:state>
      <groundspeak:short_description html="True"></groundspeak:short_description>
      <groundspeak:long_description html="True"></groundspeak:long_description>
      <groundspeak:encoded_hints></groundspeak:encoded_hints>
      <groundspeak:logs>
        <groundspeak:log id="-2">
          <groundspeak:date>2014-05-22T08:00:00</groundspeak:date>
          <groundspeak:type>Write note</groundspeak:type>
          <groundspeak:finder id="0">GSAK</groundspeak:finder>
          <groundspeak:text encoded="False">
          </groundspeak:text>
        </groundspeak:log>
      </groundspeak:logs>
      <groundspeak:travelbugs></groundspeak:travelbugs>
    </groundspeak:cache>
  </extensions>
"""

WPTEXTENSIONDEFAULTS = {
    "UserFlag": "false",
    "Lock": "false",
    "DNF": "false",
    "Watch": "false",
    "UserData": "",
    "FirstToFind": "false",
    "User2": "",
    "User3": "",
    "User4": "",
    "County": "",
    "UserSort": 0,
    "SmartName": "",
    "LastGpxDate": "",
    "Code": "",
    "Resolution": "",
    "IsPremium": "",
    "FavPoints": 0,
    "GcNote": "",
    "Guid": "",
    "CacheImages": "",
    "LogImages": "",
    "CustomData": ""
}

class GSAKWaypoint(GPXWaypoint):

    def __init__(self, latitude, longitude, extensions=None, *args, **kws):
        GPXWaypoint.__init__(self, latitude, longitude, args, kws)
        self.wptExtensions = WPTEXTENSIONDEFAULTS
        if extensions is None:
            self.extensions = None
        else:
            self.extensions = extensions

        # process extension keys, if any
        used = []
        for kw, value in kws.items():
            print kw, value
            if kw in WPTEXTENSIONDEFAULTS.keys():
                self.wptExtensions[kw] = value
                used.append(kw)
        # remove used keys
        for kw in used:
            del kws[kw]

    def __str__(self):
        s = GPXWaypoint.__str__(self)
        s += self._wptExtension()
        return s

    def _wptExtension(self):
        return WPT_EXTENSIONS % self.wptExtensions

    def to_xml(self, version):
        s = GPXWaypoint.to_xml(self, version)
        s = s.replace("</wpt>", self._wptExtension() + "</wpt>", 1)
        return s

p1 = GSAKWaypoint(1.0, 2.0)
print p1
print p1.to_xml(1)

p2 = GSAKWaypoint(1.0, 2.0, Code="Code", County="Saint Louis")
print p2.to_xml(1)

if __name__ == '__main__':

    import sys
    import os
    import traceback
    import optparse
    import time

#from pexpect import run, spawn

# Uncomment the following section if you want readline history support.
#import readline, atexit
#histfile = os.path.join(os.environ['HOME'], '.TODO_history')
#try:
#    readline.read_history_file(histfile)
#except IOError:
#    pass
#atexit.register(readline.write_history_file, histfile)

########################################################################

    def main():

        global options, args

########################################################################

    try:
        START_TIME = time.time()

        PARSER = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version=__VERSION__
        )

        PARSER.add_option(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        (OPTIONS, ARGS) = PARSER.parse_args()

        #   if len(ARGS) < 1:
        #       PARSER.error ('missing argument')

        if OPTIONS.verbose:
            print time.asctime()

        EXIT_CODE = main()

        if EXIT_CODE is None:
            EXIT_CODE = 0

        if OPTIONS.verbose:
            print time.asctime()
            print 'TOTAL TIME IN MINUTES:',
            print (time.time() - START_TIME) / 60.0

        sys.exit(EXIT_CODE)

    except KeyboardInterrupt, error_exception:        # Ctrl-C
        raise error_exception

    except SystemExit, error_exception:               # sys.exit()
        raise error_exception

    except Exception, error_exception:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(error_exception)
        traceback.print_exc()
        os._exit(1)

# end of file
