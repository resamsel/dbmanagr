#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "dbnav",
    version = "0.2",

    packages = find_packages('src', exclude=['tests']),
    package_dir = {'':'src'},
    package_data = {
        'src/images': ['*.png']
    },

    test_suite = "dbnav.tests.load_suite",

    # dependencies
    install_requires = [
        'sqlalchemy>=0.8.2',
        'psycopg2>=2.5.1'
    ],

    entry_points = {
        'console_scripts': [
            'dbnav = dbnav.navigator:main'
        ]
    },
    
    author = "René Samselnig",
    author_email = "me@resamsel.com",
    description = "The database navigator for the command line",
    keywords = "database navigator postgres sqlite"
)
