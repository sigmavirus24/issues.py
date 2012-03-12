#!/usr/bin/env python

# test_issues.py -- unittests for the Issues class in issues.py
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
from issues import Issues

class Issues_Test(base.Base):
    def _test_base_(self, i, owner, project):
        i.cache()
        self.add_to_cache('{0}-{1}.json'.format(owner, project))
        self.assertTrue(i.successful())

    def test_add_project(self):
        for (owner, project) in self.iter_repos():
            i = Issues()
            i.add_project(owner, project)
            i.fetch_issues(check_cache=True, cache_dir='./')
            self._test_base_(i, owner, project)

    def test_initialization(self):
        for (owner, project) in self.iter_repos():
            i = Issues(owner=owner, project=project)
            i.fetch_issues(check_cache=True, cache_dir='./')
            self._test_base_(i, owner, project)

    def test_cache(self):
        for (owner, project) in self.iter_repos():
            i = Issues(owner=owner, project=project)
            i.fetch_issues(check_cache=True, cache_dir='./')
            self.assertTrue(i.cached)  # Check the internal variable
