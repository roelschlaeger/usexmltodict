"""
usage: tk6.py [--help --verbose --version] [-abcdefgh] [INFILE]

Perform selected processing on .gpx files based on Tkinter GUI.

    DESCRIPTION:  GUI package using Tkinter in place of wx
    AUTHOR:       Robert Oelschlaeger <roelsch2009@gmail.com>

positional arguments:
    INFILE

optional arguments:
  --help         show this help message and exit
  -v, --verbose  show more information
  --version      show program's version number and exit

  -a
  -b
  -c
  -d
  -e
  -f
  -g
  -h

"""

from docopt import docopt

VERSION = "0.0.1"
REVISION_DATE = "20180417"
VERSION_TEXT = f"tk6.py  Version: {VERSION}  Date: {REVISION_DATE}"


def main():
    arguments = docopt(__doc__, version=VERSION_TEXT, help=False)
    if arguments["--help"]:
        print(__doc__.strip())
        return
    print(arguments)

if __name__ == "__main__":
    main()

# end of file
