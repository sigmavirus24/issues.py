#!/usr/bin/env python

import sys
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] in ("submit", "publish"):
    os.system("python setup.py sdist upload")
    sys.exit()

packages = []
requires = ['github3.py>=0.1a1']

script = 'issues.py'
#entry_points = {
#        'console_scripts': [
#            'issues.py = bin.issues:main',
#            ]
#        }

__version__ = ''
with open(script, 'r') as fd:
    reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    for line in fd:
        m = reg.match(line)
        if m:
            __version__ = m.group(1)
            break

if not __version__:
    raise RuntimeError('Cannot find version information')

setup(
    name="issues.py",
    version=__version__,
    description="A small python script to manage/track issues on GitHub",
    long_description="\n\n".join([open("README.rst").read(), 
        open("HISTORY.rst").read()]),
    author='Ian Cordasco',
    author_email="graffatcolmingov@gmail.com",
    url="https://issuespy.rtfd.org/",
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
    install_requires=requires,
    scripts=[script],
    # entry_points=entry_points,
    )
