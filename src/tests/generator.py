#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path, makedirs
import codecs

from dbnav.writer import Writer


def params(dir, testcase):
    with codecs.open(
            path.join(dir, 'resources/%s' % testcase),
            encoding='utf-8',
            mode='r') as f:
        return map(lambda line: line.strip(), f.readlines())


def expected(dir, testcase):
    with codecs.open(
            path.join(dir, 'resources/expected/%s' % testcase),
            encoding='utf-8',
            mode='r') as f:
        return f.read()


def write_actual(command, testcase, content):
    try:
        makedirs(path.join('target/actual/%s' % command))
    except:
        pass
    with codecs.open(
            path.join('target/actual/%s/%s' % (command, testcase)),
            encoding='utf-8',
            mode='w') as f:
        f.write(content)
    return content


def update_expected(dir, testcase, content):
    with codecs.open(
            path.join(dir, 'resources/expected/%s' % testcase),
            encoding='utf-8',
            mode='w') as f:
        f.write(content)
    return content


def test_generator(f, command, dir, tc, parameters=None):
    if parameters is None:
        parameters = []

    def test(self):
        p, e = params(dir, tc), expected(dir, tc)
        items = f.run([
            command,
            '-l', 'debug',
            '-L', 'target/dbnavigator.log'] + parameters + p)
        actual = Writer.write(items)
        write_actual(command, tc, actual)

        # WARNING: this is code that creates the expected output - only
        # uncomment when in need!
        # e = update_expected(dir, tc, actual)

        self.assertEqual(e, actual)
    return test
