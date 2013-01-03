#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# subfields.py: benchmarking different subfield handling strategies
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

    >>> a = 'Start^xX part^yY part^zEnd'
    >>> expand(a)
    [('_', 'Start'), ('x', 'X part'), ('y', 'Y part'), ('z', 'End')]
    >>> b = '123456'
    >>> expand(b)
    [('_', '123456')]
    >>> c = '^xX part^yY part^zEnd'
    >>> expand(c)
    [('_', ''), ('x', 'X part'), ('y', 'Y part'), ('z', 'End')]

To turn these results into a dictionary for quicker access::

    >>> da = dict(expand(a))
    >>> da['_']
    'Start'
    >>> da['y']
    'Y part'

==========================================
Subfield access using regular expressions
==========================================

Here is a field occurrence with a "Start" before any subfield marker,
and three subfield markers (^x, ^y, ^z)::

    >>> a = 'Start^xX part^yY part^zEnd'

To get specific subfield contents use get_sub::
    
    >>> get_sub(a, 'x')
    'X part'
    >>> get_sub(a, 'z')
    'End'

If a subfield marker is absent, '' is returned, but another default may be
provided::

    >>> get_sub(a, 'w')
    ''
    >>> get_sub(a, 'w', None) is None
    True

To get the text preceding the first subfield, or the entire field if 
there are no subfields, use the '*' character::

    >>> get_sub(a, '*')
    'Start'
    >>> get_sub(b, '*')
    '123456'

However, if there is no text preceding the first subfield, '*' returns 
the contents of the first subfield, like it does in the ISIS Formatting
Language::

    >>> get_sub(c, '*')
    'X part'

To avoid ambiguity of '*', use the '_' special character. It returns 
returns the default value when no text is found before the first
subfield:
    
    >>> get_sub(c, '_')
    ''
    >>> get_sub(c, '_', None) is None
    True

Otherwise, '_' behaves like '*'::

    >>> get_sub(a, '_')
    'Start'
    >>> get_sub(b, '_')
    '123456'

Here is what happens if the given content is empty::

    >>> get_sub('', '*')
    ''
    >>> get_sub('', '*', '?')
    '?'
    >>> get_sub('', '_')
    ''
    >>> get_sub('', '_', '?')
    '?'

===================
Pathological cases
===================

Both current implementations accept some characters not in [a-zA-Z0-9]
as subfield marker (characters that are meaningful in regexes may 
cause problems)::

    >>> z = 'Start^#X part^yY part^zEnd'
    >>> get_sub_r(z, '#')
    'X part'
    >>> get_sub_x(z, '#')
    'X part'
    
A '^' cannot appear as a subfield marker::
    
    >>> z = 'Start^xX part^^Y part^zEnd'
    >>> get_sub_r(z, '^', 'what?') # returns default
    'what?'
    >>> get_sub_x(z, '^', 'what?') # returns default
    'what?'
    
Empty subfields are returned as default:
    
    >>> z = 'Start^xX part^y^zEnd'
    >>> get_sub_r(z, 'y')
    ''
    >>> get_sub_r(z, 'y', 'what?') # returns default
    'what?'
    >>> get_sub_x(z, 'y')
    ''
    >>> get_sub_x(z, '^', 'what?') # returns default
    'what?'
    >>> z = 'Start^xX part^yY part^z'
    >>> get_sub_r(z, 'z')
    ''
    >>> get_sub_x(z, 'z')
    ''
    
A subfield prefix withoud a marker character at the end of the content 
is ignored::

    >>> z = 'Start^xX part^yY part^'
    >>> get_sub_r(z, 'y')
    'Y part'
    >>> get_sub_x(z, 'y')
    'Y part'
    >>> expand(z)
    [('_', 'Start'), ('x', 'X part'), ('y', 'Y part')]
    
    >>> z = '^'
    >>> get_sub_r(z, 'y')
    ''
    >>> get_sub_x(z, 'y')
    ''
    >>> expand(z)
    [('_', '')]

    
'''

import re

FIRST_SUBFIELD_RE = re.compile(r'\^[a-zA-Z0-9]([^^]*)')

def get_sub_r(content, marker, default=''):
    field_start = '^' if marker in '_*' else '\^'+marker.lower()
    regex = re.compile(r'%s([^^]*)' % field_start)
    found = regex.search(content)
    if found:
        res = found.group(1)
        if len(res) > 0:
            return res
        elif marker == '*':
            found = FIRST_SUBFIELD_RE.search(content)
            if found:
                return found.group(1)
    return default
        
def expand(content):
    parts = ('_'+content).split('^')
    return [(p[0],p[1:]) for p in parts if p]
    
def get_sub_x(content, marker, default=''):
    parts = expand(content)
    dic = dict(parts)
    if marker != '*':
        return dic.get(marker) or default
    else:
        res = dic['_']
        if len(res) > 0:
            return res
        elif len(parts) > 1:
            return parts[1][1]
    return default
    
get_sub = get_sub_x

def benchmark(func_name):
    from timeit import Timer
    n = 10**5
    setup = '''from __main__ import %s''' % func_name
    proc = func_name + '''('Start^xX part^yY part^zEnd',%r)'''
    arg = 'x'
    t = Timer(proc % arg, setup)
    print(proc % arg, t.timeit(n))
    arg = '*'
    t = Timer(proc % arg, setup)
    print(proc % arg, t.timeit(n))


if __name__=='__main__':
    import doctest
    doctest.testmod()
    #benchmark('get_sub_r')
    #benchmark('get_sub_x')

