# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import codecs
import time

import pymysql

class BiliFansInfoPipeline:

    def __init__(self):
        self.now = int(time.time())
        # 转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
        self.timeArray = time.localtime(self.now)
        self.otherStyleTime = time.strftime("%Y-%m-%d", self.timeArray)
        self.f = codecs.open('/Users/huanghuixiong/Documents/result/bili_result/fans_follows_%s.json'%(self.otherStyleTime), 'a+', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.f.write(line)
        return item

    def spider_close(self, spider):
        self.f.close()


class To_save_mysql:

    def __init__(self):
        self.connect = pymysql.connect(host='localhost', user='root', password='05693358', db='bili', port=3306)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        mid = item['mid']
        for all_fans_content in item['fans_content']:
            if all_fans_content['data']['list']:
                fans_count = all_fans_content['data']['total']
                # for content1 in all_fans_content['data']['list']:
                #     fans_name = content1['uname']
                #     fans_mid = content1['mid']
                self.cursor.execute('insert into user_mid_fans(mid,fans_name,fans_mid,fans_count,crawl_time)values ({},"{}",{},{},{})'.format(mid,
                                                                                                                                          # fans_name
                                                                                                                                        # fans_mid
                                                                                                                                          fans_count,
                                                                                                                                          int(time.time())))
        for all_follows_content in item['follows_content']:
            if all_follows_content['data']['list']:
                follows_count = all_follows_content['data']['total']
                # for content2 in all_follows_content['data']['list']:
                #     follows_name = content2['uname']
                #     follows_mid = content2['mid']
                self.cursor.execute('insert into user_mid_follower(mid,followers_name,followers_mid,followers_count,crawl_time)values ({},"{}",{},{},{})'.format(mid,
                                                                                                                                                             # follows_name,
                                                                                                                                                             # follows_mid,
                                                                                                                                                             follows_count,
                                                                                                                                                             int(time.time())))
        self.connect.commit()

    def spider_closed(self,spider):
        self.cursor.close()
        self.connect.close()


