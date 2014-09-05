#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from dbnav.writer import TestWriter

def parent_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-f', '--logfile', default='/tmp/dbnavigator.log', help='the file to log to')
    parser.add_argument('-l', '--loglevel', default='warning', help='the minimum level to log')
    return parser

def format_group(parser, test_writer=TestWriter):
    group = parser.add_argument_group('formatters')
    group.add_argument('-t', '--test', help='output format: test specific', dest='formatter', action='store_const', const=test_writer)
    return group
