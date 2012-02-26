#!/usr/bin/env python

# issues.py
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

from sys import version_info
if version_info >= (3, 0):
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
else:
    from urllib2 import Request, urlopen, HTTPError
import json
from base64 import b64encode

class GitHub(object):
    """Basic API Interface."""

    def __init__(self, user=None, pw=None, oauth_token=None):
        self.req = None
        self.auth = None
        self.last_url = None
        self.headers = None
        self.code = None
        self.data = None
        if user and pw:
            self.add_basic_auth(user, pw)
        elif oauth_token:
            self.add_oauth(oauth_token)


    def __request__(self):
        response = None
        self.req = Request(self.last_url)
        if self.auth:
            self.req.add_header('Authorization', self.auth)
        try:
            response = urlopen(self.req)
        except HTTPError as error:
            response = error
        self.headers = response.headers
        self.code = response.getcode()
        self.data = response.read()


    def add_basic_auth(self, user, pw):
        """Adds basic authentication to the object."""
        self.auth = ' '.join(['Basic', b64encode(':'.join([user, pw]))])


    def add_oauth(self, oauth_token):
        """Adds oauth authentication to the object."""
        self.auth = ' '.join(['token', oauth_token])

    
    def get_code(self):
        """Return the HTTP code for the last request."""
        return self.code


    def get_data(self):
        """Return the stored data received from the last request."""
        return self.data


    def get_headers(self):
        """Return the stored headers object."""
        return self.headers


    def get_url(self):
        """Return the stored url used by the last request."""
        return self.last_url


    def request(self, url=None):
        """Send a GET request to the GitHub API."""
        if url and url.startswith('https://api.github.com/'):
            self.last_url = url
        elif not (self.last_url or url):
            print('All requests must be made to "https://api.github.com/"')
            return
        self.__request__()


    def set_url(self, url):
        """Set url to use for requests."""
        self.last_url = url


class IssuesParser(object):
    """Handles the parsing of issues"""

    def __init__(self, data=None):
        self.flat_data = None  # The string returned by the call to the API
        self.structured_data = None  # The data structure returned by json.loads()
        self.issues_dict = {}  # Dictionary to keep the issues in
        self.issue_numbers = []  # Sorted list of issue numbers
        self.formatted = []

        if data:
            self.parse(data)


    def __parse__(self, data):
        self.flat_data = data.decode()
        self.structured_data = json.loads(self.flat_data)
        for d in self.structured_data:
            self.issues_dict[d['number']] = d
            self.issue_numbers.append(d['number'])
            self.issue_numbers.sort()


    def get_flat_data(self):
        return self.flat_data


    def parse(self, data):
        if isinstance(data, str):
            self.__parse__(data)
        elif isinstance(data, GitHub):
            self.__parse__(data.get_data())


    def format_issues(self):
        """Format the issues that were just parsed and place them in a list."""
        format_str = '{num:>3} {title} ({author}) {extra}'
        if self.issues_dict and self.issue_numbers:
            for n in self.issue_numbers:
                title = self.issues_dict[n]['title']
                author = self.issues_dict[n]['user']['login']
                assignee = None

                if self.issues_dict[n]['assignee']:
                    assignee = self.issues_dict[n]['assignee']['login']
                labels = '@{0} '.format(assignee) if assignee else '' 
                for l in self.issues_dict[n]['labels']:
                    labels = ''.join([labels, '+', l['name'], ' '])

                if self.issues_dict[n]['milestone']:
                    mile = self.issues_dict[n]['milestone']
                    labels = ''.join([labels, '#{', mile['title'], ' - ',
                            str(mile['due_on']), '}'])
                self.formatted.append(format_str.format(num=n, title=title, author=author,
                    extra=labels))


    def print_issues(self):
        """Print the issues."""
        self.format_issues()
        for issue in self.formatted:
            print(issue)


class Issues(object):
    """Provides an easy interface to the Issues list."""

    def __init__(self, owner=None, project=None, user=None, pw=None,
            oauth_token=None):
        self.github = GitHub()
        self.issues = IssuesParser()
        self.owner = None
        self.project = None
        self.url = None
        self.my_issues = None
        self.cached = False

        if owner and project:
            self.owner = owner
            self.project = project
            self.url = 'https://api.github.com/repos/{owner}/{proj}/issues'
            self.url = self.url.format(owner=self.owner, proj=self.project)
            self.github.set_url(self.url)
        if user:
            self.user = user
            self.my_issues = 'https://api.github.com/issues'
            if pw:
                self.github.add_basic_auth(user, pw)
            if not self.github.get_url():
                self.github.set_url(self.my_issues)
        if oauth_token:
            self.github.add_oauth(oauth_token)


    def cache(self, cache_dir='.'):
        if self.cached:
            return
        if self.owner and self.project:
            filename = '{0}/{1}-{2}.json'.format(cache_dir, self.owner, self.project)
        elif self.user:
            filename = '{0}/{1}.json'.format(cache_dir, self.user)
        with open(filename, 'w+') as fd:
            fd.write(self.issues.get_flat_data())


    def __search_for__(self, owner, project, cache_dir):
        from os import listdir, stat
        from time import time
        name = '{0}-{1}.json'.format(owner, project)
        for f in listdir(cache_dir):
            if f == name:
                s = stat(f)
                s = int(time() - s.st_ctime)/60
                if s < 60:
                    self.cached = True
                    return f
        return None


    def fetch_issues(self, owner=None, project=None, check_cache=False,
            cache_dir=None):
        if check_cache:
            owner = owner or self.owner
            project = project or self.project
            f = self.__search_for__(owner, project, cache_dir)
            if self.cached:
                self.open_cache(f)
                return

        url = None
        if owner and project:
            url = 'https://api.github.com/repos/{owner}/{proj}/issues'
            url = url.format(owner=owner, proj=project)

        self.github.request(url)
        if self.github.get_code() == 200:
            self.issues.parse(self.github)
        else:
            print("{0} error: {1}.".format(self.github.get_code(),
                self.github.get_url()))


    def print_issues(self):
        self.issues.print_issues()


    def open_cache(self, filename):
        with open(filename, 'r') as fd:
            self.issues.parse(fd.read())
