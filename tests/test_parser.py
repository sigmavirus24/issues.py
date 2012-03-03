#!/usr/bin/env python

# test_parser.py -- parser test class for unittests designed for issues.py
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

import base
from issues import IssuesParser

class IssuesParser_Test(base.Base):
    def setUp(self):
        self.clint_data = open('tests/json-clint', 'r').read()
        self.todo_data = open('tests/json-todo.py', 'r').read()
        self.fabric_data = open('tests/json-fabric', 'r').read()
        super(IssuesParser_Test, self).setUp()

    def test_static_data(self):
        pass
