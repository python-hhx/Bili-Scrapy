# -*- coding: utf-8 -*-
# @Author  : HHX
# @Time    : 2020/9/10 16:23
# @FileName: run.py

from scrapy import cmdline

cmdline.execute("scrapy crawl fans_info".split())