#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# subfields2.py: parsing subfields with regular expressions
#
# Copyright (C) 2010 BIREME/PAHO/WHO
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


'''
===========================================================
Expanding a string into subfields prepended with ^ markers
===========================================================

Common case::

    >>> expand('Start^xX part^yY part^zEnd')
    [('_', 'Start'), ('x', 'X part'), ('y', 'Y part'), ('z', 'End')]

Subfield keys are case-insensitive, always stored in lowercase::

    >>> expand('Start^XX part^YY part^ZEnd')
    [('_', 'Start'), ('x', 'X part'), ('y', 'Y part'), ('z', 'End')]


No subfield markers::

    >>> expand('Start')
    [('_', 'Start')]

Empty leading subfield::

    >>> expand('^xX part^yY part^zEnd')
    [('_', ''), ('x', 'X part'), ('y', 'Y part'), ('z', 'End')]

Empty field::

    >>> expand('')
    [('_', '')]

The optional `codes` argument specifies acceptable subfield marker codes::

    >>> expand('Start^xX part^yY part^zEnd', 'xyz')
    [('_', 'Start'), ('x', 'X part'), ('y', 'Y part'), ('z', 'End')]
    >>> expand('Start^xX part^yY part^zEnd', 'abc')
    [('_', 'Start^xX part^yY part^zEnd')]

Invalid subfield marker is ignored (content is appendend to previous subfield)::

    >>> expand('Start^xX part^!Y part^zEnd')
    [('_', 'Start'), ('x', 'X part^!Y part'), ('z', 'End')]
    >>> expand('Start^xX part^yY part^zEnd', 'yz')
    [('_', 'Start^xX part'), ('y', 'Y part'), ('z', 'End')]
    >>> expand('Start^xX part^yY part^zEnd', 'xy')
    [('_', 'Start'), ('x', 'X part'), ('y', 'Y part^zEnd')]
    >>> expand('Start^^X part^yY part^zEnd')
    [('_', 'Start^'), ('x', ' part'), ('y', 'Y part'), ('z', 'End')]
    >>> expand('Start^xX part^yY part^')
    [('_', 'Start'), ('x', 'X part'), ('y', 'Y part^')]

'''

import re

SUBFIELD_MARKER_RE = re.compile(r'\^([a-zA-Z0-9])')

def expand(content, codes=None):
    if codes is None:
        subfield_re = SUBFIELD_MARKER_RE
    else:
        subfield_re = re.compile(r'\^([%s])' % codes)
    parts = []
    start = 0
    key = '_'
    while True:
        found = subfield_re.search(content, start)
        if found is None: break
        parts.append((key, content[start:found.start()]))
        key = found.group(1).lower()
        start = found.end()
    parts.append((key, content[start:]))
    return parts


if __name__=='__main__':
    import doctest
    doctest.testmod()

