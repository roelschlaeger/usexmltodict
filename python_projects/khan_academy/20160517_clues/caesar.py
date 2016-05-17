# coding=utf-8

"""Compute Caesar cipher encoding/decoding."""

from __future__ import print_function
import string

########################################################################

UPPER = string.ascii_uppercase

########################################################################


def caesar(s, n):
    """Perform Caesar ROT-'n' encoding on string 's'."""
    out = []
    for c in s.upper():
        if c in UPPER:
            n2 = (UPPER.find(c) + n) % len(UPPER)
            out.append(UPPER[n2])
        else:
            out.append(" ")
    return "".join(out)

########################################################################


def caesars(s):
    """Perform caesar decoding for all values of n."""
    print("   %s" % s)
    print("   %s" % ("=" * len(s)))
    for n in range(len(UPPER)):
        print("%-2d %s" % (n, caesar(s, n)))

########################################################################

if __name__ == '__main__':

    def main(args):
        """Perform Caesar encoding for a test string."""
        """Determine if args.string is a list or a string"""
        args_list = args.string
        """If it is a strings, make it a list"""
        if isinstance(args_list, str):
            print("Single string detected")
            args_list = list(args_list)
        else:
            print("List detected")

        """Process each string in the args_list list"""
        for s in args_list:
            caesars(s)
            print()

########################################################################

    from argparse import ArgumentParser

    PARSER = ArgumentParser(
        prog=None,
        usage=None
    )

    PARSER.add_argument(
        "string",
        nargs="*",
        default=["The quick brown fox jumped over the lazy dog."]
    )

    args = PARSER.parse_args()

    main(args)

########################################################################

# end of file
