#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time

logger = logging.getLogger(__name__)

def logduration(subject, start):
    logger.info('%s took: %0.6fs', subject, time.time() - start)
