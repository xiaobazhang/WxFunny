# -*- coding: utf-8 -*-
# !/usr/bin/python
#
# File name: auth
# Author: suli
# Date created: 17/10/14
# Python Version: 2.7
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import time
from hashlib import sha1


class WeChatAuth(object):
    def __init__(self, token, min_seconds, max_seconds):
        '''
        bucket will delete nonce which overtime then min_seconds
        '''
        self.min_seconds = min_seconds
        self.max_seconds = max_seconds
        self.token = token
        self.bucket = {}
        self.clean_time = int(time.time())

    def authorized(self, signature, timestamp, nonce):
        if not self.fill_bucket(timestamp, nonce): return False
        if (sha1("".join(sorted([self.token,
                                 str(timestamp),
                                 nonce]))).hexdigest() ==
                signature):
            return True
        return False

    def fill_bucket(self, timestamp, nonce):
        now = int(time.time())
        if not ((now - self.min_seconds) <=
                    timestamp <=
                    (now + self.max_seconds)):
            return False

        if (now - self.clean_time) >= self.min_seconds:
            self.clean_bucket(now - self.min_seconds)
        if self.bucket.has_key(nonce): return False
        self.bucket[nonce] = timestamp
        return True

    def clean_bucket(self, timestamp):
        new_bucket = {}
        for k, v in self.bucket.iteritems():
            if v >= timestamp: new_bucket[k] = v
        self.bucket = new_bucket
