# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import codecs
import json
import time
import re

import pymysql


class BiliUserInfoDynamicPipeline:
    def __init__(self):
        self.now = int(time.time())
        #转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
        self.timeArray = time.localtime(self.now)
        self.time_1 = time.strftime("%Y-%m-%d", self.timeArray)
        self.file_1 = codecs.open('/Users/huanghuixiong/Documents/result/bili_result/bili_user_dynamic%s.json' % (self.time_1), 'a+', encoding='utf-8')

    def process_item(self, item, spider):
        if 'all_dynamic' in dict(item):
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.file_1.write(line)
            return item
        else:
            return item

    def spider_closed(self, spider):
        self.file.close()
        self.file_1.close()


class To_save_sql:

    def __init__(self):
        self.connect = pymysql.connect(host='localhost', user='root', password='05693358', db='bili', port=3306)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        pattern = re.compile(r'"')
        if 'all_dynamic' in dict(item):
            mid = item['mid']
            sex = item['sex']
            birthday = item['birthday']
            sign = re.sub(pattern, '', item['sign'])
            for content_1 in item['all_dynamic']:
                content = ''
                reply = 0
                like = 0
                view = 0
                keys = content_1.keys()
                try:
                    name = content_1['user']['uname']
                except:
                    name = ''
                if 'title' in keys:
                    content = re.sub(pattern, '', content_1['title'])
                elif 'item' in keys:
                    if 'content' in content_1['item'].keys():
                        content = re.sub(pattern, '', content_1['item']['content'])
                        if 'reply' in content_1['item'].keys():
                            reply = content_1['item']['reply']
                    elif 'description' in content_1['item'].keys():
                        content = re.sub(pattern, '', content_1['item']['description'])
                        reply = content_1['item']['reply']
                elif 'stat' in keys:
                    reply = content_1['stat']['reply']
                    like = content_1['stat']['like']
                    view = content_1['stat']['view']
                elif 'desc' in keys:
                    content = re.sub(pattern, '', content_1['desc'])
                if content:
                    self.cursor.execute('insert into user_mid_dynamic(mid,name,sex,birthday,sign,dynamic_title,comment_count,like_count,play_count,crawl_time)values \
                                        ({},"{}","{}","{}","{}","{}",{},{},{},{})'.format(mid, name, sex, birthday, sign, content, reply, like, view, int(time.time())))

                    self.connect.commit()
            return item


        def spider_closed(self, spider):
            self.cursor.close()
            self.connect.close()

