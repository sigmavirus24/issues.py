#!/usr/bin/env python

# base.py -- base class for unittests designed for issues.py
# Copyright (C) 2012  Sigmavirus24
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# TLDR: This is licensed under the GPLv3. See LICENSE for more details.

import os
import re
import sys
import unittest
import issues

class BaseCase(unittest.TestCase):
    repositories = {'sigmavirus24': ['Todo.txt-python'], 'kennethreitz':
            ['clint', 'requests', 'httpbin'], 'osteele10': ['jetsam'], 'fabric':
            ['fabric'], 'rupa': ['sprunge'], 'tpope': ['vim-pathogen']}  # More to be added
    cache_files = []

    def setUp(self):
        self.backupstdout, sys.stdout = sys.stdout, os.devnull
        self.issues = Issues()

    def tearDown(self):
        self.stdout = self.backupstdout

    def add_to_cache(self, filename):
        self.cache_files.append(filename)

    def assert_cache_was_written(self, filename):
        for node in os.listdir(self.issues.get_cache_dir()):
            self.assertEquals(node, filename)
