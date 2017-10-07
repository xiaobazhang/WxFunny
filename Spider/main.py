# -*- coding: utf-8 -*-
#!/usr/bin/python
#
# File name: main
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

import spider_url
from spider_sina import sina
from spider_config import config, sql


def main():
    sql.create_table()
    sina(config, sql)
    sina.spider_with_all_page()
    print "END"


if __name__ == '__name__':
    main()
