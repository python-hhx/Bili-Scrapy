#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author： huanghuixiong
# datetime： 2020/11/4 12:03 下午 
# filename: run.py
# ide： PyCharm

from scrapy.cmdline import execute


execute('scrapy crawl user_article'.split())