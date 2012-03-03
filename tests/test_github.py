#!/usr/bin/env python

# test_github.py -- unittests for the GitHub class in issues.py
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
from issues import GitHub

class GitHub_Test(base.Base):
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
        self.__test_code__('users/nevereverever', 404, '{"message":"Not Found"}')


    def test_valid_repository(self):
        for (user, repos) in self.repositories.items():
            for repo in repos:
                path = 'repos/{u}/{r}'.format(u=user, r=repo)
                self.__test_code__(path, 200)


    def test_valid_user(self):
        for user in self.repositories:
            self.__test_code__('users/{u}'.format(u=user), 200)


    def test_set_url(self):
        url = self.ghurl('repos/sigmavirus24')
        github = GitHub()
        github.set_url(url)
        self.assertEquals(github.geturl(), url)

    def test_auth(self):
        auth = ('sigmavirus24', 'fakepassword')
        oauth = 'oauth_token_clearly_not_real'
        # Basic Authentication at initialization
        github = GitHub(*auth)
        self.assertTrue(github.using_auth())
        # Basic Authorization after initialization
        github = GitHub()
        self.assertFalse(github.using_auth())
        github.add_basic_auth(*auth)
        self.assertTrue(github.using_auth())
        # OAuth Authorization at initialization
        github = GitHub(oauth_token=oauth)
        self.assertTrue(github.using_auth())
        # OAuth Authorization after initialization
        github = GitHub()
        github.add_oauth(oauth)
        self.assertTrue(github.using_auth())
