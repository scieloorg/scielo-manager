#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# ID file reader (.id is a format exported by the CISIS mx tool)
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

import re

# sample: !ID 0000002
RECORD_START_RE = re.compile(r'^!ID (\d+)$')
# sample: !v004!ADOLEC
FIELD_START_RE = re.compile(r'^!v(\d+)!(.*)$')

RECORD_ID_KEY = '_id' # key for the record id, such as MFN

def reader(id_file, lin_count=0):
    ''' generator which reads records from the open id_file provided '''
    record = {}
    field_tag = None
    for lin in id_file:
        lin_count += 1
        field_start = FIELD_START_RE.match(lin)
        if field_start:
            if record:
                field_tag, content = field_start.groups()
                field_occurrences = record.setdefault(field_tag,[])
                field_occurrences.append(content)
            else:
                msg = '(Line %s) Invalid field start, no previous record ID: %r'
                raise ValueError(msg % (lin_count, lin[:20]))
        else:           
            rec_start = RECORD_START_RE.match(lin)
            if rec_start:
                if record:
                    yield record
                record = {RECORD_ID_KEY: rec_start.group(1)}
                field_tag = None
            elif field_tag is not None:
                # append to last field ocurrence and remove trailing newline for
                # consistency with regex matches which don't include the newline
                record[field_tag][-1] += '\n'+ lin.rstrip('\n')
            else:
                msg = '(Line %s) Invalid line, no previous field tag: %r'
                raise ValueError(msg % (lin_count, lin[:20]))

    if record:
        yield record
            
def test():
    import doctest
    doctest.testfile('idfile_test.txt')

if __name__=='__main__':
    test()
        


                
                
