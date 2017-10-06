# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# File name: spider_sina
# Author: suli
# Date created: 10/4/17
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
from selenium import webdriver
from spider_config import config,sql

class sina_rsult:
    def __init__(self):
        self.web = ""
        self.tag = ""
        self.url = ""
        self.content = ""
        self.path = ""


class sina:
    def __init__(self, config, sql):
        self.config = config
        self.sql = sql
        self.driver = webdriver.PhantomJS(executable_path=self.config.phantomjs_path)


    def spider_sina_feature(self):
        gif_feed_box = self.driver.find_elements_by_class_name('gif_feed_box')
 



    def spider_with_one_page(self):
        self.driver.get(self.config.spider_url['sina'])
