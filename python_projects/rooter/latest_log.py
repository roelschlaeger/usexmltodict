#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

"""
DESCRIPTION

    This function returns log information for a given wpt.

EXAMPLES

    Show some examples of how to use this script.

EXIT STATUS

    List exit codes

AUTHOR

    Robert Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

"""

from __future__ import print_function

import sys
from pprint import pprint

assert sys.version_info > (3, ), "Python 3 required"

########################################################################


__VERSION__ = "0.0.2"
__DATE__ = "2017-07-28"

########################################################################

CACHETAG = '{http://www.groundspeak.com/cache/1/0/1}cache'
DATETAG = '{http://www.groundspeak.com/cache/1/0/1}date'
LOGSTAG = '{http://www.groundspeak.com/cache/1/0/1}logs'
LOGTAG = '{http://www.groundspeak.com/cache/1/0/1}log'
TEXTTAG = '{http://www.groundspeak.com/cache/1/0/1}text'
TYPETAG = '{http://www.groundspeak.com/cache/1/0/1}type'

EXTTAG = '{http://www.topografix.com/GPX/1/1}extensions'

#   http://www.topografix.com/GPX/1/1
#       http://www.topografix.com/GPX/1/1/gpx.xsd
#   http://www.groundspeak.com/cache/1/0/1
#       http://www.groundspeak.com/cache/1/0/1/cache.xsd
#   http://www.gsak.net/xmlv1/6
#       http://www.gsak.net/xmlv1/6/gsak.xsd

########################################################################


def latest_log(wpt):
    """Get log information for the wpt waypoint

    returns a dict containing:

        count:
            a count of the number of logs

        most_recent_find_date
            a string containing the GSAK data of the most recent "Found It" log

        recent_log_types
            a list of log "Type" strings of these kinds
                "Found It"
                "Maintenance Required"
                "Didn't Find It"
                "Write Note"

        most_recent_log
            a string containing the most recent log string

    """

    # default return value
    result = {
        "count": 0,
        "most_recent_find_date": "",
        "recent_log_types": [],
        "most_recent_log": "",
    }

    # locate the extension
    wpt_extension = wpt.find(EXTTAG)
    if wpt_extension is None:
        return result

    cache = wpt_extension.find(CACHETAG)
    if cache is None:
        return result

    groundspeak_logs = cache.find(LOGSTAG)
    if groundspeak_logs is None:
        return result

    cache_logs = groundspeak_logs.findall(LOGTAG)
    if cache_logs is None:
        return result

    if not cache_logs:
        return result

    result["count"] = len(cache_logs)

    result["recent_log_types"] = \
        types_list = \
        [x.find(TYPETAG).text for x in cache_logs]

    result["most_recent_log"] = cache_logs[0].find(TEXTTAG).text

    try:
        most_recent_find_index = types_list.index("Found it")
        result["most_recent_find_date"] = \
            cache_logs[most_recent_find_index].find(DATETAG).text
    except ValueError:
        pass

    return result

########################################################################


if __name__ == '__main__':

    import argparse
    import time

########################################################################

    # CACHETAG = '{http://www.groundspeak.com/cache/1/0/1}cache'
    # EXTTAG = '{http://www.topografix.com/GPX/1/1}extensions'
    # LOGSTAG = '{http://www.groundspeak.com/cache/1/0/1}logs'
    # LOGTAG = '{http://www.groundspeak.com/cache/1/0/1}log'

    # def make_tag(element, _tag):
    #     """Replace the tag in L{element} with L{_tag}."""
    #     tag = element.tag
    #     index = tag.find("}")
    #     old_tag = tag[index + 1:]
    #     new_tag = tag.replace(old_tag, _tag)
    #     return new_tag

    def main(args, _options):
        """Main routine for testing."""

        from rooter import get_wpts
        wpts, _junk = get_wpts(args[0])
        for wpt in wpts:
            result = latest_log(wpt)
            if result["count"]:
                pprint(result)
                print()

        return 0

########################################################################

    import textwrap

    try:
        START_TIME = time.time()

        PARSER = argparse.ArgumentParser(
            usage=textwrap.dedent(__doc__)
        )

        PARSER.add_argument(
            "--version",
            action="version",
            version="%%(prog)s: Version %s %s" % (__VERSION__, __DATE__)
        )

        PARSER.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        PARSER.add_argument("files", nargs="*")

        OPTIONS = PARSER.parse_args()
        ARGS = OPTIONS.files

        if len(ARGS) < 1:
            # PARSER.error ('missing argument')
            # ARGS = [r"C:/Users/Robert Oelschlaeger/Dropbox/Geocaching/"
            #     r"topo731 - Poplar Bluff MO/"
            #     r"topo731b - Poplar Bluff MO.gpx"]
            ARGS = ["default.gpx"]

        if OPTIONS.verbose:
            print(time.asctime())

        EXIT_CODE = main(ARGS, OPTIONS)

        if EXIT_CODE is None:
            EXIT_CODE = 0

        if OPTIONS.verbose:
            print(time.asctime())
            print('TOTAL TIME IN MINUTES:',)
            print((time.time() - START_TIME) / 60.0)

        sys.exit(EXIT_CODE)

    except KeyboardInterrupt as _error:      # Ctrl-C
        raise _error

    except SystemExit as _error:             # sys.exit()
        raise _error

    # except Exception as _error:
    #     print('ERROR, UNEXPECTED EXCEPTION')
    #     print(str(_error))
    #     traceback.print_exc()
    #     os._exit(1)

# end of file
