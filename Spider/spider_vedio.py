# -*- coding: utf-8 -*-
# !/usr/bin/python
#
# File name: spider_vedio
# Author: suli
# Date created: 17/10/8
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

from browsermobproxy import Server
import time
from spider_config import config, sql
from selenium import webdriver


class vedio:
    def __init__(self, config, sql):
        #   设置网络链路监控
        self.server = Server(config.browsermob_proxy)
        self.server.start()
        self.proxy = self.server.create_proxy()
        self.CHROME_OPTIONS = {"profile.managed_default_content_settings.images": 2}
        print self.proxy.port
        '''
        self.proxy_address = "--proxy=127.0.0.1:%s" % self.proxy.port
        self.service_args = [self.proxy_address, '--ignore-ssl-errors=yes', ]
        self.driver = webdriver.PhantomJS(executable_path=config.phantomjs_path, service_args=self.service_args)
        '''
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--proxy-server={host}:{port}'.format(host="localhost", port=self.proxy.port))
        self.chrome_options.add_experimental_option("prefs", self.CHROME_OPTIONS)
        self.driver = webdriver.Chrome(
            executable_path=config.chrome_path,
            chrome_options=self.chrome_options)

    def set_control_url(self, url):
        self.proxy.new_har(url)

    def get_data(self, url):
        self.driver.get(url)
        time.sleep(5)
        data = self.proxy.har
        return data

    def handle_data(self, content):
        video_box = []
        data = content['log']['entries']
        for j in range(len(data)):
            url = data[j]['request']['url']
            print url
            video_box.append(url)

    def __del__(self):
        self.server.stop()
        self.driver.close()
