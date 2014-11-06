#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
