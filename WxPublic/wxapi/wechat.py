# -*- coding: utf-8 -*-
# !/usr/bin/python
#
# File name: wechat
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


from hashlib import sha1
import urllib
import time

from auth import WeChatAuth
from message import WCMessage

MIN_SECONDS = 30
MAX_SECONDS = 30

EVENT_DEFAULT = "default"
EVENT_MSG = "event"
COMMAND_MSG = "command"
TEXT_MSG = "text"


class WeChatServer(object):
    def __init__(self, token):
        self.handlers = {}
        self.handler_default = None
        self.has_command = False
        self.token = token
        self.auth = WeChatAuth(token, MIN_SECONDS, MAX_SECONDS)

    def authorized(self, signature, timestamp, nonce):
        return self.auth.authorized(signature, timestamp, nonce)

    def register_default(self, handler):
        self.handler_default = handler

    def register_message(self, name, handler):
        self.handlers[name] = handler

    def register_event(self, event, handler, key=EVENT_DEFAULT):
        if not self.handlers.has_key(EVENT_MSG): self.handlers[EVENT_MSG] = {}
        if not self.handlers[EVENT_MSG].has_key(event):
            self.handlers[EVENT_MSG][event] = {}
        self.handlers[EVENT_MSG][event][key] = handler

    def register_command(self, command, handler):
        self.has_command = True
        if not self.handlers.has_key(COMMAND_MSG):
            self.handlers[COMMAND_MSG] = {}
        self.handlers[COMMAND_MSG][command.lower()] = handler

    def feed(self, data):
        msg = WCMessage(data)
        handler = self.handlers.get(msg.get('MsgType', ""))
        if handler:
            if msg.get('MsgType', "") == COMMAND_MSG:
                handler = handler.get(msg.get('Event'))
                if handler:
                    handler = handler.get(msg.get('EventKey') or EVENT_DEFAULT)
            elif (self.has_command and
                          msg.get('MsgType', "") == TEXT_MSG and
                      msg.has_key('Content')):
                cs = msg['Content'].split(" ")
                if len(cs) >= 2:
                    command = cs[0].lower()
                    handler = self.handlers[COMMAND_MSG].get(command, handler)
                    msg['Content'] = " ".join(cs[1:])
        handler = handler or self.handler_default
        if not handler: return None
        return handler(msg)
