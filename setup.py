#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import expanduser

setup(
    name = "dbnav",
    version = "0.6",

    packages = find_packages('src', exclude=['tests']),
    package_dir = {'':'src'},
    package_data = {
        'src/images': ['*.png']
    },

    test_suite = 'dbnav.tests.load_suite',

    # dependencies
    install_requires = [
        'sqlalchemy>=0.8.2',
        'psycopg2>=2.5.1'
    ],

    entry_points = {
        'console_scripts': [
            'dbnav = dbnav.navigator:main',
            'dbexport = dbnav.exporter:main',
            'dbgraph = dbnav.grapher:main',
            'dbexec = dbnav.executer:main'
        ]
    },
    
    data_files = [
        (expanduser('~/.bash_completion.d'), ['src/bash_completion/dbnav'])
    ],
    
    author = "René Samselnig",
    author_email = "me@resamsel.com",
    description = "The database navigator for the command line",
    keywords = "database navigator exporter grapher postgres sqlite graphviz"
)
