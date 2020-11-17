import scrapy
from urllib.parse import urlencode
import json
import redis
from bili_user_info.items import BiliUserInfoItem


class BbSpider(scrapy.Spider):
    name = 'bb'
    allowed_domains = ['api.bilibili.com']
    start_urls = ['https://api.bilibili.com/x/space/acc/info?']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    all_page_content = []
    count_dict = {}
    content_dict = {}
    all_video_type = {}
    #f = open(r'C:\Users\phhx223\Desktop\result\bb.json', 'r', encoding='utf-8')
    #f = open('/Users/huanghuixiong/Documents/result/bili_result/all_memeber_1.json', 'r', encoding='utf-8')
    server = redis.Redis(host='127.0.0.1', port=6379, password='', db=3)

    def start_requests(self):
        # for line in self.f:
        #     dict_1 = json.loads(line)
        #     mid = dict_1['mid']
        key = "video_mid"
        while (self.server.llen(key)>0):
            mid = self.server.rpop(key)
            data = {
                'mid': mid,
                'jsonp': 'jsonp'
            }
            url = self.start_urls[0] + urlencode(data)
            dict_1 = {'mid': mid}
            self.content_dict.setdefault(mid, [])
            self.count_dict.setdefault(mid, 0)
            self.all_video_type.setdefault(mid, [])
            yield scrapy.FormRequest(url=url, callback=self.parse_info, meta=dict_1, headers=self.headers, dont_filter=True)

    def parse_info(self, response):
        item = BiliUserInfoItem()
        mid = response.meta['mid']
        all_content = json.loads(response.text)
        item['mid'] = mid
        item['sex'] = all_content['data']['sex']  # 性别
        item['birthday'] = all_content['data']['birthday']  # 生日
        item['sign'] = all_content['data']['sign']  # 个人签名
        item['all_video_info'] = []
        url = 'https://api.bilibili.com/x/space/arc/search?'
        self.count_dict[mid] = self.count_dict[mid] + 1
        data = {
            'mid': mid,
            'ps': '30',
            'tid': '0',
            'pn': self.count_dict[mid],
            'keyword': '',
            'order': 'pubdate',
            'jsonp': 'jsonp'
        }
        url_1 = url + urlencode(data)
        dict_1 = {'mid': mid, 'item': item}
        yield scrapy.FormRequest(url=url_1, headers=self.headers, meta=dict_1, callback=self.parse_video, dont_filter=True)

    def parse_video(self, response):
        item = response.meta['item']
        mid = response.meta['mid']
        all_video_content = json.loads(response.text)['data']['list']['vlist']
        if all_video_content:
            print(len(self.content_dict[mid]))
            all_content = json.loads(response.text)['data']['list']['vlist']
            # 新增了用户类型
            if not self.all_video_type[mid]:
                self.all_video_type[mid].append(json.loads(response.text)['data']['list']['tlist'])
            for content_1 in all_content:
                self.content_dict[mid].append(content_1)
            url = 'https://api.bilibili.com/x/space/arc/search?'
            data = {
                'mid': mid,
                'ps': '30',
                'tid': '0',
                'pn': self.count_dict[mid],
                'keyword': '',
                'order': 'pubdate',
                'jsonp': 'jsonp'
            }
            url_1 = url + urlencode(data)
            dict_1 = {'mid': mid, 'item': item}
            self.count_dict[mid] += 1
            yield scrapy.FormRequest(url=url_1, headers=self.headers, meta=dict_1, callback=self.parse_video,
                                     dont_filter=True)

        else:
            print(len(self.content_dict[mid]))
            item['all_video_info'] = self.content_dict[mid]
            item['all_video_type'] = self.all_video_type[mid]
            self.content_dict[mid] = []
            self.all_video_type[mid] = []
            yield item

