# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# File name: spider_thread
# Author: suli
# Date created: 9/24/17
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
import spider_config


url = 'http://gif.sina.com.cn/'
conf = spider_config.config()
conf.init()
driver = webdriver.PhantomJS(executable_path=conf.phantomjs_path)

driver.get(url)

time.sleep(1)

gif_feed_box = driver.find_elements_by_class_name('gif_feed_box')

for i in gif_feed_box:
    h2 = i.find_element_by_tag_name('h2')
    gif_url = h2.find_element_by_tag_name('a').get_attribute('href')
    gif_content = h2.find_element_by_tag_name('a').text
    ul = i.find_element_by_tag_name('ul')
    gif_tag = ul.find_element_by_tag_name('li').find_element_by_tag_name('a').text
    print gif_url
    print gif_content
    print gif_tag




driver.close()

