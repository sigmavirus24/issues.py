#!/usr/bin/env python

import sys
import shutil
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] in ("submit", "publish"):
    os.system("python setup.py sdist upload")
    sys.exit()

packages = []
requires = ['github3.py>=0.1a']

from issues import __version__, __author__
script = 'issues.py'

setup(
    name="issues.py",
    version=__version__,
    description="A small python script to manage/track issues on GitHub",
    long_description="\n\n".join([open("README.rst").read(), 
        open("HISTORY.rst").read()]),
    author=__author__,
    author_email="graffatcolmingov@gmail.com",
    url="https://github.com/sigmavirus24/issues.py",
    package_data={'': ['LICENSE']},
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Utilities',
        ),
    scripts=[script],
    )
