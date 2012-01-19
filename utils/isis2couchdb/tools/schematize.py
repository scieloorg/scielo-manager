#!/usr/bin/env python
# coding: utf-8

# schematize.py: an ISIS-DM schema source code generator
#
# Copyright (C) 2010 BIREME/OPAS/OMS
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

import sys
import json
import re
import argparse

SUBFIELD_MARKER_RE = re.compile(r'\^([a-zA-Z0-9])')
MAX_CANDIDATE_KEY_LEN = len('36a62682-c4f2-11df-ac2d-0bee4063ebba')

class FieldStats(object):
    def __init__(self, tag):
        self.tag = tag
        self.frequency = 0 # number of records where field occurs
        self.occurrences = 0 # total number of field occurrences, in all records
        self.min_occurrences = sys.maxsize # min. and max. number of...
        self.max_occurrences = 0           # ...occurences in a record
        self.min_len = sys.maxsize  # min. and max length of...
        self.max_len = 0            # ...individual ocurrences
        self.subfields = {}
        self.numeric = True # assume it's numeric until proven otherwise
        self.candidate_key = True # assume unique until proven otherwise
        self.values = set()
        
    def update(self, occurrences):
        self.frequency += 1
        self.min_occurrences = min(self.min_occurrences, len(occurrences))
        self.max_occurrences = max(self.max_occurrences, len(occurrences))
        if len(occurrences) > 1:
            self.candidate_key = False
            self.values = None
        for occ in occurrences:
            self.occurrences += 1
            self.min_len = min(self.min_len, len(occ))
            self.max_len = max(self.max_len, len(occ))
            self.numeric = self.numeric and occ.isdigit()
            if (self.candidate_key and
                    len(occ) <= MAX_CANDIDATE_KEY_LEN and
                    occ not in self.values):
                self.values.add(occ)
            else:
                self.candidate_key = False
                self.values = None
            for sub in SUBFIELD_MARKER_RE.findall(occ):
                self.subfields[sub] = self.subfields.get(sub, 0) + 1
        
    def dump(self, attrs=None):
        res = {}
        if attrs is None:
            attrs = self.__dict__
        for key in attrs:
            if key.startswith('_'): continue
            value = getattr(self, key)
            if isinstance(value,type(lambda:0)): continue
            res[key] = value
        return repr(res)
        
    def __repr__(self):
        return self.dump('tag frequency'.split())

    def is_numeric(self):
        return self.numeric
        
    def is_repeating(self):
        return self.max_occurrences > 1
        
    def is_fixed_len(self):
        return self.max_len == self.min_len
        
    def subfield_markers(self):
        return ''.join(sorted(self.subfields))
        
    def subfield_freqs(self):
        return sorted(self.subfields.items())
        
    def subfield_freqs_pct(self):
        tot = float(self.occurrences)
        return [(k,f,f/tot*100) for (k, f) in sorted(self.subfields.items())]

def statistics(records, filter_tag=None, filter_value=None):
    stats = {}
    analysed = 0
    for rec in records:
        if filter_tag:
            if (filter_tag not in rec) or (rec[filter_tag][0] != filter_value):
                continue
        analysed += 1
        for tag in rec:
            try:
                ntag = int(tag)
            except ValueError:
                continue # skip non-numeric tags
            fstat = stats.setdefault(ntag, FieldStats(ntag))
            fstat.update(rec[tag])
    return (len(records), analysed, stats)
    
PROPERTY_TPL = '''{spaces}{name} = {class}(tag={tag}{options})'''

def schematize(records, filter_tag=None, filter_value=None, quorum=0, indent=4):
    total, analysed, stats = statistics(records, filter_tag, filter_value)
    code = []
    candidate_key_fields = 0
    rare_fields = 0
    generated_fields = 0
    for tag, field in sorted(stats.items()):
        if str(tag) == filter_tag:
            continue  # skip field used for type filtering
        if field.frequency < quorum: # skip seldom used fields
            rare_fields += 1
            continue 
        specs = {'class': 'PluralProperty' if field.is_repeating() 
                                           else 'SingularProperty'}
        specs['name'] = 'v%02d' % field.tag
        specs['tag'] = repr(str(field.tag))
        options = []
        if field.frequency == analysed:
            options.append(('required', True))
        if field.candidate_key:
            options.append(('unique', True))
            candidate_key_fields += 1
        subs = field.subfield_markers()
        if subs:
            options.append(('subfields', repr(subs)))
        # TODO: validators should be a list of funcions
        if field.is_numeric():
            options.append(('numeric', True))
        if field.is_fixed_len():
            options.append(('fixed_len', field.max_len))
        specs['spaces'] = ' '*indent
        if options:
            prefix = ',\n' + ' '*(indent+16)
            options = ['{0}={1}'.format(option, value) 
                            for (option, value) in options]
            specs['options'] = ', ' + prefix.join(options)
        else:
            specs['options'] = ''
        code.append(PROPERTY_TPL.format(**specs))
        generated_fields += 1
    if code:
        class_name = 'Type' + filter_value if filter_value else 'SampleType'
        class_stmt = 'class %s(CheckedModel):' % class_name
        code.insert(0, class_stmt)
        code.append('\n# {0} records analyzed out of {1} total records'
                        .format(analysed, total))
        code.append('# {0} properties generated out of {1} distinct tags found'
                        .format(generated_fields, len(stats)))                       
        code.append('# {0} candidate key properties detected'.format(candidate_key_fields))
        if filter_tag:
            code.append('# filter tag {0} omitted from model'.format(filter_tag))
        if rare_fields:
            code.append('# {0} uncommon tags omitted from model'.format(rare_fields))

    return '\n'.join(code)

def test(verbose):
    import doctest
    res = doctest.testfile('schematize_test.txt', verbose=verbose)
    print res

if __name__=='__main__':

    # create the parser
    parser = argparse.ArgumentParser(
        description='Generate ISIS-DM schema from a'
                    ' sample database in ISIS-JSON format')

    parser.add_argument('file_name', 
        metavar='INPUT.json', nargs='?', default='', 
        help='.json file to read')
    parser.add_argument('-f', '--filter', metavar='TAG:TYPE',
        help='use TAG to filter only records of TYPE')
    parser.add_argument('-q', '--quorum', type=int, default=0,
        help='min. frequency required to generate a property from a tag'
             ' (useful to ignore uncommon tags)')
    parser.add_argument('-t', '--test', 
        action='store_true', help='run tests (ignore input file)')
    parser.add_argument('-v', '--verbose-tests', 
        action='store_true', help='run verbose tests (ignore input file)')
    
    # parse the command line
    args = parser.parse_args()
    if args.test or args.verbose_tests:
        test(args.verbose_tests)
    elif args.file_name:
        if args.filter:
            try:
                filter_tag, filter_value = args.filter.split(':')
            except ValueError: # wrong tuple size to unpack
                print('ERROR: -f option must be formatted like -f 9:A')
                parser.print_usage()
                raise SystemExit
        else:
            filter_tag = filter_value = None
        with open(args.file_name) as input:
            db = json.load(input)
            print(schematize(db, filter_tag, filter_value, quorum))
    else:
        parser.print_usage()
