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

import unittest
import base
from issues import GitHub


class GitHub_Test(base.BaseCase):
    def test_invalid_url(self):
        github = GitHub()
        github.request('http://www.example.com')
        self.assertEquals(github.geturl(), None)


    def __test_code__(self, url, code, data=None):
        url = self.ghurl(url)
        github = GitHub()
        github.request(url)
        self.assertEquals(github.getcode(), code)
        self.assertEquals(github.geturl(), url)
        if data:
            self.assert_bytes_equals(github.getdata(), data)


    def test_invalid_userpassword(self):
        url = self.ghurl('user')
        github = GitHub('test', 'password')
        github.request(url)
        self.assertEquals(github.getcode(), 401)
        self.assert_bytes_equals(github.getdata(), '{"message":"Bad credentials"}')


    def test_invalid_repository(self):
        self.__test_code__('repos/sigmavirus24/fakerepo', 404, 
            '{"message":"Not Found"}')


    def test_invalid_user(self):
        self.__test_code__('users/nevereverever', 404)


    def test_valid_repository(self):
        self.__test_code__('repos/sigmavirus24/issues.py', 200)


    def test_valid_user(self):
        self.__test_code__('users/sigmavirus24', 200)
