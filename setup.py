#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "dbnav",
    version = "0.1",

    packages = find_packages('src/main'),
    package_dir = {'':'src/main'},
    package_data = {
        'src/images': ['*.png']
    },

    # dependencies
    install_requires = [
        'sqlalchemy>=0.8.2',
        'psycopg2>=2.5.1'
    ],

    entry_points = {
        'console_scripts': [
            'dbnav = dbnav.navigator:main'
        ]
    }
)
