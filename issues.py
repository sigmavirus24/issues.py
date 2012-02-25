#!/usr/bin/env python

from sys import version_info
if version_info >= (3, 0):
    from urllib.request import Request, urlopen
    from urllib.error import HTTPError
else:
    from urllib2 import Request, urlopen, HTTPError
import json
from base64 import b64encode

class GitHub(object):
    req = None
    auth = None

    def __init__(self, user=None, pw=None, oauth_token=None):
        if user and pw:
            b64 = b64encode(':'.join([user, pw]))
            self.auth = ' '.join(['Basic', b64])
        elif oauth_token:
            self.auth = ' '.join(['token', oauth_token])


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

    
    def get_code(self):
        """Return the HTTP code for the last request."""
        return self.code


    def get_data(self):
        """Return the stored data received from the last request."""
        return self.data


    def get_url(self):
        """Return the stored url used by the last request."""
        return self.last_url


    def request(self, url=None):
        if url and url.startswith('https://api.github.com/'):
            self.last_url = url
        elif not (self.last_url or url):
            print('All requests must be made to "https://api.github.com/"')
            return
        self.__request__()
