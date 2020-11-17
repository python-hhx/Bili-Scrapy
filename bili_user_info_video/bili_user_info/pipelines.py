import codecs
import json
import time
import re

import pymysql


class BiliUserInfoPipeline(object):
    def __init__(self):
        self.now = int(time.time())
        #转换为其他日期格式,如:"%Y-%m-%d %H:%M:%S"
        self.timeArray = time.localtime(self.now)
        self.time_1 = time.strftime("%Y-%m-%d", self.timeArray)
        self.file = codecs.open('/Users/huanghuixiong/Documents/result/bili_result/bili_user_video_%s.json' % (self.time_1), 'a+', encoding='utf-8')
        #self.file_1 = codecs.open('/Users/huanghuixiong/Documents/result/bili_result/bili_user_dynamic%s.json' % (self.time_1), 'a+', encoding='utf-8')

    def process_item(self, item, spider):
        if spider.name == 'bb':
            if 'all_video_info' in dict(item):
                line = json.dumps(dict(item), ensure_ascii=False) + '\n'
                self.file.write(line)
                return item
            else:
                return item
        else:
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
        pattern = re.compile('(\d+)')
        if spider.name =='bb':
            if 'all_video_info' in dict(item):
                for all_content in item['all_video_info']:
                    if 'int' in str(type(item['mid'])):
                        mid = item['mid']
                    else:
                        mid = int(re.findall(pattern, str(item['mid']))[0])

                    if 'int' in str(type(all_content['comment'])):
                        comment = all_content['comment']
                    else:
                        comment = 0

                    if 'int' in str(type(all_content['play'])):
                        play = all_content['play']
                    else:
                        play = 0
                    try:
                        self.cursor.execute('insert into user_mid_video(mid,name,video_id,title,title_desc,comment_count,play_count,creat_time,video_length,crawl_time)values \
                                            ({},"{}","{}","{}","{}",{},{},{},"{}",{})'.format(mid,
                                                                                         all_content['author'].replace('"', "").replace("'", ""),
                                                                                         all_content['bvid'],
                                                                                         all_content['title'].strip().replace('"', "").replace("'", "").replace("\n", ","),
                                                                                         all_content['description'].replace('"', "").replace("'", "").replace("\n", ","),
                                                                                         comment,
                                                                                         play,
                                                                                         all_content['created'],
                                                                                         all_content['length'],
                                                                                         int(time.time())))
                    except:
                        self.cursor.execute('insert into user_mid_video(mid,name,video_id,title,title_desc,comment_count,play_count,creat_time,video_length,crawl_time)values \
                                            ({},"{}","{}","{}","{}",{},{},{},"{}",{})'.format(mid,
                                                                                         all_content['author'].replace('"', "").replace("'", ""),
                                                                                         all_content['bvid'],
                                                                                         '含有特殊符号无法入库',
                                                                                         '含有特殊符号无法入库',
                                                                                         comment,
                                                                                         play,
                                                                                         all_content['created'],
                                                                                         all_content['length'],
                                                                                         int(time.time())))

                    self.connect.commit()
        return item


    def spider_closed(self, spider):
        self.cursor.close()
        self.connect.close()


