import scrapy
from urllib.parse import urlencode
import json
import redis

from bili_user_info_dynamic.items import BiliUserInfoDynamicItem


class BiliVideoSpider(scrapy.Spider):
    name = 'bili_dynamic'
    allowed_domains = ['api.bilibili.com']
    start_urls = ['https://api.bilibili.com/x/space/acc/info?']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    all_page_content = []
    offset_id_dict = {}
    content_dict = {}
    count_id_dict = {}
    all_mid_list = []
    #f = open('/Users/huanghuixiong/Documents/result/bili_result/all_memeber_dynamic.json', 'r', encoding='utf-8')
    server = redis.Redis(host='127.0.0.1', port=6379, password='', db=3)

    def start_requests(self):
        key = "article_mid"
        while (self.server.llen(key) > 0):
            mid = self.server.rpop(key)
            if mid not in self.all_mid_list:
                self.all_mid_list.append(mid)
                data = {
                    'mid': mid,
                    'jsonp': 'jsonp'
                }
                url = self.start_urls[0] + urlencode(data)
                dict_1 = {'mid': mid}
                self.content_dict.setdefault(mid, [])
                self.offset_id_dict.setdefault(mid, 0)
                self.count_id_dict.setdefault(mid, 0)
                yield scrapy.FormRequest(url=url, callback=self.parse_info, meta=dict_1, headers=self.headers,
                                         dont_filter=True)

    def parse_info(self, response):
        item = BiliUserInfoDynamicItem()
        mid = response.meta['mid']
        all_content = json.loads(response.text)
        item['mid'] = mid
        item['sex'] = all_content['data']['sex']  # 性别
        item['birthday'] = all_content['data']['birthday']  # 生日
        item['sign'] = all_content['data']['sign']  # 个人签名
        item['all_dynamic'] = []
        url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?'
        data_1 = {
            'visitor_uid': '0',
            'host_uid': mid,  # 用户ID
            'offset_dynamic_id': self.offset_id_dict[mid],  # 此部分的ID可以通过返回的json获取下一页内容
            'need_top': '1',
        }
        url_1 = url + urlencode(data_1)
        dict_1 = {'mid': mid, 'item': item}
        yield scrapy.FormRequest(url=url_1, headers=self.headers, meta=dict_1, callback=self.parse_dynamic,
                                 dont_filter=True)

    def parse_dynamic(self, response):
        item = response.meta['item']
        mid = response.meta['mid']
        all_dynamic_content = json.loads(response.text)['data']
        if all_dynamic_content['next_offset'] != 0:
            if ('next_offset' in all_dynamic_content):
                self.offset_id_dict[mid] = all_dynamic_content['next_offset']
                for page_num_1 in range(len(all_dynamic_content['cards'])):
                    content_2 = all_dynamic_content['cards'][page_num_1]['card']
                    self.content_dict[mid].append(json.loads(content_2))
                self.count_id_dict[mid] += 1
                url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?'
                data_1 = {
                    'visitor_uid': '0',
                    'host_uid': mid,  # 用户ID
                    'offset_dynamic_id': self.offset_id_dict[mid],  # 此部分的ID可以通过返回的json获取下一页内容
                    'need_top': '1',
                }
                url_1 = url + urlencode(data_1)
                dict_1 = {'mid': mid, 'item': item}
                yield scrapy.FormRequest(url=url_1, headers=self.headers, meta=dict_1, callback=self.parse_dynamic,
                                         dont_filter=True)
        else:
            print(len(self.content_dict[mid]))
            item['all_dynamic'] = self.content_dict[mid]
            yield item
