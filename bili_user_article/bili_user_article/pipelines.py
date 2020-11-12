# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql
import time
import re


class BiliUserArticlePipeline:

    def __init__(self):
        self.connect = pymysql.connect(host='localhost', user='root', password='05693358', db='bili', port=3306)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        pattern = re.compile('(\d+)')
        if 'int' in str(type(item['mid'])):
            mid = item['mid']
        else:
            mid = int(re.findall(pattern, str(item['mid']))[0])

        if 'int' in str(type(item['view'])):
            view = item['view']
        else:
            view = 0

        if 'int' in str(type(item['reply'])):
            reply = item['reply']
        else:
            reply = 0

        if 'int' in str(type(item['like'])):
            like = item['like']
        else:
            like = 0

        if 'int' in str(type(item['share'])):
            share = item['share']
        else:
            share = 0

        self.cursor.execute('insert into user_mid_article(mid,name,article_title,article_id,article_view,article_reply,article_like,article_share,article_publish_time,crawl_time)values \
                                          ({},"{}","{}",{},{},{},{},{},"{}",{})'.format(mid,
                                                                                         item['author'],
                                                                                         item['article_title'],
                                                                                         item['article_id'],
                                                                                         view,
                                                                                         reply,
                                                                                         like,
                                                                                         share,
                                                                                         item['publish_time'],
                                                                                         int(time.time())))
        self.connect.commit()
        return item

    def spider_closed(self, spider):
        self.cursor.close()
        self.connect.close()


