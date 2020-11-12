import scrapy
import json
import redis
from urllib.parse import urlencode
from bili_fans_info.items import BiliFansInfoItem


class FansInfoSpider(scrapy.Spider):
    name = 'fans_info'
    allowed_domains = ['api.bilibili.com']
    start_urls = ['http://api.bilibili.com/']
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    #f = open(r'C:\Users\phhx223\Desktop\result\all_bad_user_mid.json', 'r', encoding='utf-8')
    f = open(r'/Users/huanghuixiong/Documents/result/bili_result/all_memeber_1.json', 'r', encoding='utf-8')
    fans_count = {}
    fans_content = {}
    follow_count = {}
    follow_content = {}
    server = redis.Redis(host='127.0.0.1', port=6379, password='', db=3)

    def start_requests(self):
        url = 'https://api.bilibili.com/x/relation/followers?'
        key = "fans_follows"
        while (self.server.llen(key) > 0):
            mid = self.server.rpop(key)
            # mid = json.loads(user_info)['mid']
            self.fans_count.setdefault(mid, 0)
            self.fans_content.setdefault(mid, [])
            for page_num in range(1, 6):
                data = {
                    'vmid': mid,
                    'pn': page_num,
                    'ps': '20',
                    'order': 'desc',
                    'jsonp': 'jsonp'
                }
                new_url = url + urlencode(data)
                yield scrapy.FormRequest(url=new_url, headers=self.headers, callback=self.parse_1, meta={'mid': mid})


    def parse_1(self, response):
        mid = response.meta['mid']
        all_fans_content = json.loads(response.text)
        self.fans_count[mid] += 1
        self.fans_content[mid].append(all_fans_content)
        url = 'https://api.bilibili.com/x/relation/followings?'
        self.follow_count.setdefault(mid, 0)
        self.follow_content.setdefault(mid, [])
        for page_num in range(1, 6):
            data = {
                'vmid': mid,
                'pn': page_num,
                'ps': '20',
                'order': 'desc',
                'jsonp': 'jsonp'
            }
            new_url = url + urlencode(data)
            yield scrapy.FormRequest(url=new_url, headers=self.headers, callback=self.parse_2, meta={'mid': mid})


    def parse_2(self, response):
        mid = response.meta['mid']
        item = BiliFansInfoItem()
        all_follows_content = json.loads(response.text)
        self.follow_content[mid].append(all_follows_content)
        self.follow_count[mid] += 1
        if (self.fans_count[mid] == 5) and (self.follow_count[mid] == 5):
            item['mid'] = mid
            item['fans_content'] = self.fans_content[mid]
            item['follows_content'] = self.follow_content[mid]
            yield item