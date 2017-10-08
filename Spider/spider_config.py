#-*-coding:utf-8 -*-
#!/usr/bin/python
#
#  File name: spider_config
#  Author: suli
#  Date created: 10/2/17
#  Python Version: 2.7
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


import platform
import logging
import os
import sqlite3
import spider_tool


class config:
    system_version = "Linux"
    work_dir = ""
    log_name = ""
    db_name = ""
    dir_list = []
    phantomjs_path = ""
    spider_url = {
        'sina': 'http://gif.sina.com.cn/'
    }
    max_spider_page = 50

    def __init__(self):
        config.init(self)

    def init(self):
        config.system_version = platform.system()
        if config.system_version == "Windows":
            config.work_dir = 'C://spider/'
        elif config.system_version == "Linux":
            home = os.getenv('HOME')
            config.work_dir = home + '/spider'
        elif config.system_version == "Darwin":
            config.work_dir = os.getenv('HOME') + '/spider'
        else:
            print "error: not find system version!"

        # 设置日志名称
        config.log_name = "spider.log"
        # 设置DB名字
        config.db_name = "spider.db"
        # 设置工作目录结构
        config.dir_list = ['/log', '/pic', '/vedio', '/article', '/db']
        # 设置phantomjs的程序路径
        config.phantomjs_path = '/Users/suli/soft/phantomjs/bin/phantomjs'
        # 创建工作子目录
        for i in config.dir_list:
            spider_tool.create_dir(config.work_dir + i)
            print (config.work_dir + i)
        # 初始化日志
        logging.basicConfig(filename=config.work_dir+"/log/"+config.log_name, level=logging.INFO,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')


class sql:
    def __init__(self, config):
        db_path = config.work_dir + "/db/" + config.db_name
        self.cont = sqlite3.connect(db_path)
        logging.info("connect sql success!!")
        self.c = self.cont.cursor()

    def create_table(self):
        try:
            result = self.c.execute('''CREATE TABLE IF NOT EXISTS SPIDER
                    (WEB            TEXT    NOT NULL,
                     TAG            TEXT    NOT NULL,
                     URL            TEXT    NOT NULL,
                     CONTENT        TEXT    NOT NULL,
                     PATH           TEXT    NOT NULL
                     );''')
            if result is not None:
                logging.info("create sqlite db succes!!")
                return True
        except:
            logging.error('create sql table error!!')
            return False
        return False

    def insert_data(self, web, tag, url, content, path):
        query = "SELECT * FROM SPIDER WHERE URL='%s'" % url
        self.c.execute(query)
        result = self.c.fetchall()
        if len(result) == 0:
            sql = "INSERT INTO SPIDER (WEB, TAG, URL, CONTENT, PATH) VALUES ('%s', '%s', '%s', '%s', '%s')" % (
            web, tag, url, content, path)
            self.c.execute(sql)
            self.cont.commit()
            logging.info("insert into spider %s,%s,%s,%s,%s", web, tag, url, content, path)
            return True
        else:
            return False

    def select_web(self, web):
        sql = "SELECT * FROM SPIDER WHERE WEB='%s'" % web
        return self.c.execute(sql)

    def select_tag(self, tag):
        sql = "SELECT * FROM SPIDER WHERE TAG='%s'" % tag
        return self.c.execute(sql)

    def select_url(self, url):
        sql = "SELECT * FROM SPIDER WHERE URL='%s'" % (url)
        return self.c.execute(sql)

    def select_content(self, content):
        sql = "SELECT * FROM SPIDER WHERE CONTENT='%s'" % (content)
        return self.c.execute(sql)

    def select_path(self, path):
        sql = "SELECT * FROM SPIDER WHERE PATH='%s'" % path
        return self.c.execute(sql)

    def delete_web(self, web):
        sql = "DELETE FROM SPIDER WHERE WEB='%s'" % web
        self.c.execute(sql)
        logging.info("delete spider web:%s", web)
        return self.cont.total_changes

    def delete_tag(self, tag):
        sql = "DELETE FROM SPIDER WHERE TAG='%s'" % tag
        self.c.execute(sql)
        logging.info("delete spider tag:%s", tag)
        return self.cont.total_changes

    def delete_url(self, url):
        sql = "DELETE FROM SPIDER WHERE URL='%s'" % url
        self.c.execute(sql)
        logging.info("delete spider url:%s", url)
        return self.cont.total_changes

    def delete_content(self, content):
        sql = "DELETE FROM SPIDER WHERE CONTENT='%s'" % content
        self.c.execute(sql)
        logging.info("delete spider content:%s", content)
        return self.cont.total_changes

    def delete_path(self, path):
        sql = "DELETE FROM SPIDER WHERE URL='%s'" % path
        self.c.execute(sql)
        logging.info("delete spider path:%s", path)
        return self.cont.total_changes