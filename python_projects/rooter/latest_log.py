#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99:fileencoding=utf-8:ft=python

# Created:       Thu 16 Jan 2014 11:25:46 AM CST
# Last Modified: Fri 17 Jan 2014 11:19:57 AM CST

"""
SYNOPSIS

    TODO latest_log [-h] [-v,--verbose] [--version]

DESCRIPTION

    TODO This function returns log information for a given wpt.

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

    import sys
    import os
    import traceback
    import optparse
    import time

########################################################################

    CACHETAG = '{http://www.groundspeak.com/cache/1/0/1}cache'
    EXTTAG = '{http://www.topografix.com/GPX/1/1}extensions'
    LOGSTAG = '{http://www.groundspeak.com/cache/1/0/1}logs'
    LOGTAG = '{http://www.groundspeak.com/cache/1/0/1}log'

    def make_tag(element, s):
        tag = element.tag
        index = tag.find("}")
        old_tag = tag[index + 1:]
        new_tag = tag.replace(old_tag, s)
        return new_tag

    from pprint import pprint

    def main():

        global options, args

        from rooter import get_wpts
        wpts, junk = get_wpts(args[0])
        for wpt in wpts:
            result = latest_log(wpt)
            if result["count"]:
                pprint(result)
                print

########################################################################

    try:
        start_time = time.time()

        parser = optparse.OptionParser(
            formatter=optparse.TitledHelpFormatter(),
            usage=globals()['__doc__'],
            version=__VERSION__
        )

        parser.add_option(
            '-v',
            '--verbose',
            action='store_true',
            default=False,
            help='verbose output'
        )

        (options, args) = parser.parse_args()

        if len(args) < 1:
#           parser.error ('missing argument')
#           args = [r"C:/Users/Robert Oelschlaeger/Dropbox/Geocaching/"
#                   r"topo731 - Poplar Bluff MO/"
#                   r"topo731b - Poplar Bluff MO.gpx"]
            args = ["default.gpx"]
#
        if options.verbose:
            print time.asctime()

        exit_code = main()

        if exit_code is None:
            exit_code = 0

        if options.verbose:
            print time.asctime()
            print 'TOTAL TIME IN MINUTES:',
            print (time.time() - start_time) / 60.0

        sys.exit(exit_code)

    except KeyboardInterrupt, e:        # Ctrl-C
        raise e

    except SystemExit, e:               # sys.exit()
        raise e

    except Exception, e:
        print 'ERROR, UNEXPECTED EXCEPTION'
        print str(e)
        traceback.print_exc()
        os._exit(1)

# end of file
