# -*- coding: utf-8 -*-
#!/usr/bin/python2.4
#
# Copyright 2007 The Python-Twitter Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys

# parse_qsl moved to urlparse module in v2.6
try:
  from urlparse import parse_qsl
except:
  from cgi import parse_qsl

import oauth2 as oauth

class AccessTokenFactory:
  def __init__(self):
    self.consumer_key      = '1uFNM4QtiqRGB1ZQGKUY8g'
    self.consumer_secret   = 'BeCH5j8ZPmum357xEF9tvVf1VttVWY2E8hpcfk0'
    self.REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
    self.ACCESS_TOKEN_URL  = 'https://api.twitter.com/oauth/access_token'
    self.AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
    self.SIGNIN_URL        = 'https://api.twitter.com/oauth/authenticate'

  def get_authorization_url(self):
    self.signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()
    self.oauth_consumer             = oauth.Consumer(key=self.consumer_key, secret=self.consumer_secret)
    self.oauth_client               = oauth.Client(self.oauth_consumer)

    self.res, self.content = self.oauth_client.request(self.REQUEST_TOKEN_URL, 'GET')

    if self.res['status'] != '200':
      print 'Invalid respond from Twitter requesting temp token: %s' % self.res['status']
    else:
      self.request_token = dict(parse_qsl(self.content))
      return '%s?oauth_token=%s' % (self.AUTHORIZATION_URL, self.request_token['oauth_token'])


  def get_access_token(self, pin):
    token = oauth.Token(self.request_token['oauth_token'], self.request_token['oauth_token_secret'])
    token.set_verifier(pin)

    self.oauth_client  = oauth.Client(self.oauth_consumer, token=token)
    res, content = self.oauth_client.request(self.ACCESS_TOKEN_URL, method='POST', body='oauth_verifier=%s' % pin)
    access_token  = dict(parse_qsl(content))

    # print self.request_token['oauth_token']
    if res['status'] != '200':
      print 'Error status: %s' % res['status']
      raise
    else:
      return (access_token['oauth_token'], access_token['oauth_token_secret'])

