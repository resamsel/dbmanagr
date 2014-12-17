#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 René Samselnig
#
# This file is part of Database Navigator.
#
# Database Navigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Database Navigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Database Navigator.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import re
import codecs
from collections import Counter

filename = sys.argv[1]

with codecs.open(filename, encoding='utf-8') as f:
    text = f.read()

m = re.findall(r'^#{2,3} .*$', text, re.MULTILINE)

def title(s):
    return re.sub(r'#+ ', '', s)
def fragment(s):
    return '#' + re.sub(r'[^a-z-]', '', re.sub(r'#+ ', '', s).replace(' ', '-').lower())
def depth(s):
    return len(re.match(r'(#*)', s).group(0))

c = Counter()

toc = []
for header in m:
    t = title(header)
    f = fragment(header)
    d = depth(header)
    
    if c[f] > 0:
        toc.append('{}- [{}]({}-{})'.format('\t'*(d-2), t, f, c[f]))
    else:
        toc.append('{}- [{}]({})'.format('\t'*(d-2), t, f))
    
    c[f] += 1

with codecs.open(filename, 'w', encoding='utf-8') as f:
    f.write(text.replace('[TOC]', '\n'.join(toc)))
