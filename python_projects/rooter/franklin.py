# coding=utf-8

"""Use the Franklin Order 8 Magic Square for encryption.

-   http://www.mathpages.com/HOME/kmath155.htm
"""

########################################################################

from __future__ import print_function

import sys
from pprint import pprint

assert sys.version_info > (3, ), "Python 3 required"

########################################################################


__VERSION__ = "0.0.101"
__DATE__ = "2017-07-30"

########################################################################

FRANKLIN = """\
52 61  4 13 20 29 36 45
14  3 62 51 46 35 30 19
53 60  5 12 21 28 37 44
11  6 59 54 43 38 27 22
55 58  7 10 23 26 39 42
 9  8 57 56 41 40 25 24
50 63  2 15 18 31 34 47
16  1 64 49 48 33 32 17
"""

########################################################################

if __name__ == "__main__":

    ########################################################################

    def build_dictionaries():
        """Build forward- and back-reference dictionaries from FRANKLIN."""
        _dictionary = {}
        _dictionary_reverse = {}

        for row_number, row in enumerate(FRANKLIN.split('\n')):

            for col_number, digits in enumerate(row.split()):

                if DEBUG:
                    print("%02d %02d %2s" % (row_number, col_number, digits))

                _temp = (row_number, col_number)
                _number = int(digits)
                _dictionary[_temp] = _number
                _dictionary_reverse[_number] = _temp

            if DEBUG:
                print()

        return _dictionary, _dictionary_reverse

    ########################################################################

    def decode(_string, _dictionary):
        """Decode string _string according to _dictionary."""
        _string = _string.upper()

        result = list("_" * 64)

        for row in range(8):
            for col in range(8):
                _temp = (row, col)
                index = _dictionary[_temp]
                result[index - 1] = _string[row * 8 + col]

        return "".join(result)

    ########################################################################

    def encode(_string, _dictionary_reverse):
        """Encode string _string according to _dictionary_reverse."""
        _string = _string.upper()

        if DEBUG:
            print(_string)

        _output = []
        for row in range(8):
            _row = []
            for col in range(8):
                _row.append("")
            _output.append(_row)

        for index, _char in enumerate(_string):

            row, col = _dictionary_reverse[index + 1]
            _output[row][col] = _char

        if DEBUG:
            pprint(_output)

        return "\n".join(["".join(_row) for _row in _output])

    ########################################################################

    def main(args, options):
        """Process each of the command line arguments."""
        global DEBUG  # pylint: disable=W0601
        DEBUG = options.debug

        _dictonary_forward, _dictionary_reverse = build_dictionaries()
        if DEBUG:
            pprint(_dictionary_reverse)

        for arg in args:

            _string = arg.replace(' ', '')
            _string += 'X' * (64 - len(_string))
            assert len(_string) == 64

            if DEBUG:
                print(_string)

            if not options.encode:
                result = decode(_string, _dictonary_forward)
            else:
                result = encode(_string, _dictionary_reverse)

            print("".join(result.split('\n')))
            print()

    ########################################################################

    from argparse import ArgumentParser
    import textwrap

    PARSER = ArgumentParser(description=textwrap.dedent(__doc__))

    PARSER.add_argument(
        "--version",
        action="version",
        version="Version: %s %s" % (__VERSION__, __DATE__)
        )

    PARSER.add_argument(
        "-d",
        "--debug",
        dest="debug",
        action="count",
        help="increment debug counter"
        )

    PARSER.add_argument(
        "-e",
        "--encode",
        dest="encode",
        action="store_true",
        help="encode"
        )

    OPTIONS = PARSER.parse_args()
    ARGS = OPTIONS.encode

    if not ARGS:
        ARGS = [
            "norththirtyeightdegreesfiftysixpointeighteighteightminutes",
            "westninetydegreesfiftyeightpointthreethreethreeminutes",
            "MXTIRSTHGRXTTNIGIXHEEYEGYTXNIITEUSHTSFGERIETTHIFHXOHEXIETNXGIOPD",
            "TXTGFOERRSXUERIIEXNETPEHDIXSTTTYXXNYEHHETEXXERGINXEEFNHEEWXIMTTS",
        ]

    main(ARGS, OPTIONS)

########################################################################
