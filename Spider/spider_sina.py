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


# 典型的sina搞笑gif的html代码
'''
    <div class="gif_feed_box">
    <h2>
        <a href="http://storage.slide.news.sina.com.cn/slidenews/77_ori/2017_40/74766_800877_921633.gif" target="_blank">养狗千日用狗一时</a>
    </h2>
    <div class="gif_img">
        <a href="javascript:;" style="display: block;" dataurl="http://storage.slide.news.sina.com.cn/slidenews/77_ori/2017_40/74766_800877_921633.gif" class="gif_img_loaded" onclick="gifTool.showBigImg(this);return;">
            <img src="http://storage.slide.news.sina.com.cn/slidenews/77_ori/2017_40/74766_800877_921633.gif" datasrc="http://storage.slide.news.sina.com.cn/slidenews/77_ori/2017_40/74766_800877_921633.gif" alt="" class="feedImg" style="height: 455px;">
            </a>
            <a href="javascript:;" class="gif_img_loading" style="display: none;">
                <img src="http://n.sinaimg.cn/tech/gif/160407/160425_loading.gif" height="70" width="70" alt="">
                </a>
            </div>
            <ul class="gif_tags clearfix">
                <li>
                    <a href="http://gif.sina.com.cn/?category=动物">动物</a>
                </li>
            </ul>
            <div class="gif_feed_a clearfix">
                <div class="left">
                    <a href="javascript:;" class="gif_like" onclick="gifTool.subCount('kj_slidenews-album-74766-493002',this)">327</a>
                    <a href="javascript:;" onclick="gifTool.showComment(this,'kj','slidenews-album-74766-493002');" class="gif_comment" dataid="kj:slidenews-album-74766-493002:0">10</a>
                </div>
                <div class="bdsharebuttonbox right bdshare-button-style1-16" data-tag="share_30" data-bd-bind="1507362546276">
                    <a class="bds_tsina" data-cmd="tsina" title="分享到新浪微博"></a>
                    <a class="bds_weixin" data-cmd="weixin" title="分享到微信"></a>
                    <a class="bds_more" data-cmd="more"></a>
                </div>
            </div>
            <div class="sina-comment-wrap"></div>
        </div>
'''


import time
from selenium import webdriver
from spider_config import config,sql
import spider_tool
import urllib
import hashlib


class sina_result:
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
        self.gif_dir_path = self.config.work_dir + "/pic/sina_gif"
        spider_tool.create_dir(self.gif_dir_path)
        self.result_map

    # 获取页上的数据
    def spider_sina_feature(self):
        gif_feed_box = self.driver.find_elements_by_class_name('gif_feed_box')
        result_list = []
        for i in range(len(gif_feed_box)):
            h2 = gif_feed_box[i].find_element_by_tag_name('h2')
            gif_url = h2.find_element_by_tag_name('a').get_attribute('href')
            gif_content = h2.find_element_by_tag_name('a').text
            ul = gif_feed_box[i].find_element_by_tag_name('ul')
            gif_tag = ul.find_element_by_tag_name('li').find_element_by_tag_name('a').text
            result = sina_result()
            result.tag = gif_tag
            result.url = gif_url
            result.content = gif_content
            result_list.append(result)

        return result_list

    def spider_with_one_page(self, url):
        self.driver.get(url)
        result = self.spider_sina_feature()
        return result

    def spider_with_all_page(self):
        page = 1
        while page:
            page_url = '#page=%d' % page
            url = self.config.spider_url['sina'] + page_url
            result = self.spider_with_one_page(url)

            for i in result:
                url = i.url
                url_md5 = hashlib.md5(url).hexdigest()  # 下载链接url的MD5作为保存名字
                save_path = self.gif_dir_path + "/%s_%s.gif" % (i.tag, url_md5)
                urllib.urlretrieve(url, save_path)
                i.web = self.config.spider_url['sina']
                i.path = save_path
                ret = self.sql.insert_data(i.web, i.tag, i.url, i.content, i.path)
                if ret is False:
                    page = 0

            self.sql.commit()  # 提交事务
