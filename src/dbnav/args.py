#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

def parent_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-f', '--logfile', default='/tmp/dbnavigator.log', help='the file to log to')
    parser.add_argument('-l', '--loglevel', default='warning', help='the minimum level to log')
    return parser

def format_group(parser):
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--test', help='output format: test specific', action='store_true')
    return group
