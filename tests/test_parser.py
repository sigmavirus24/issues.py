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
import json
from issues import IssuesParser, GitHub

class IssuesParser_Test(base.Base):
    def setUp(self):
        self.projects = set(['clint', 'todo.py', 'fabric'])

        self.data = {}
        for p in self.projects:
            self.data[p] = open('tests/json-{0}'.format(p), 'r').read()

        self.formatted = {}
        for p in self.projects:
            self.formatted[p] = open('tests/formatted-{0}'.format(p),
                    'r').readlines()
            self.formatted[p] = [l.strip('\n') for l in self.formatted[p]]

        super(IssuesParser_Test, self).setUp()

    def _parser_equiv_(self, p, parser):
        parser.format_issues()
        self.assert_list_items_equivalent(self.formatted[p],
                parser.get_formatted_items())


    def test_initialization(self):
        for p in self.projects:
            parser = IssuesParser(self.data[p])
            self.assertEquals(self.data[p], parser.get_flat_data())
            self._parser_equiv_(p, parser)

    def test_github_parse(self):
        gh = GitHub()
        for p in self.projects:
            gh.data = self.data[p]
            parser = IssuesParser()
            parser.parse(gh)
            self._parser_equiv_(p, parser)

    def test_data_parse(self):
        for p in self.projects:
            parser = IssuesParser()
            parser.parse(self.data[p])
            self._parser_equiv_(p, parser)

    def test_get_issue(self):
        for p in self.projects:
            parser = IssuesParser(self.data[p])
            json_list = json.loads(self.data[p])
            json_dict = {}
            for l in json_list:
                self.assertEquals(l, parser.get_issue(l['number']))
