#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time

def logduration(subject, start):
    logging.debug('%s took: %0.6fs' % (subject, time.time() - start))
