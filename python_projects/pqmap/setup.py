#!/usr/bin/env python
# vim:ts=4:sw=4:tw=0:wm=0:et:foldlevel=99
# -*- coding: utf-8 -*-

# Created:       Thu 02 Jan 2014 02:04:43 PM CST
# Last Modified: Mon 13 Jan 2014 07:25:25 PM CST

"""
SYNOPSIS

    setup [-h] [-v,--verbose] [--version]

DESCRIPTION

    File for use with setuptools for generation of distribution packages for
    pqmap.py.

EXAMPLES

    python setup.py

EXIT STATUS

    TODO: List exit codes

AUTHOR

    Robert L. Oelschlaeger <roelsch2009@gmail.com>

LICENSE

    This script is in the public domain.

"""

from distutils.core import setup
setup(
    name='pqmap',
    version='0.0.2',
    py_modules=[
        'kmldraw',
        'quads',
        'simplekml',
    ],
    author="Robert L. Oelschlaeger",
    author_email="roelsch2009@gmail.com",
    maintainer="Robert L. Oelschlaeger",
    maintainer_email="roelsch2009@gmail.com",
)

# vim:set sr et ts=4 sw=4 ft=python fenc=utf-8: // See Vim, :help 'modeline'
