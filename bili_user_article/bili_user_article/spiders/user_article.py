import scrapy
import json
import redis

from urllib.parse import urlencode
from bili_user_article.items import BiliUserArticleItem


class UserArticleSpider(scrapy.Spider):
    name = 'user_article'
    allowed_domains = ['api.bilibili.com']
    start_urls = ['https://api.bilibili.com/x/space/article?']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    count_dict = {}

    # f = open('/Users/huanghuixiong/Documents/result/bili_result/all_memeber_1.json', 'r', encoding='utf-8')
    server = redis.Redis(host='127.0.0.1', port=6379, password='', db=3)

    def start_requests(self):
        # for line in self.f:
        #     dict_1 = json.loads(line)
        #     mid = dict_1['mid']
        key = "article_mid"
        while (self.server.llen(key) > 0):
            mid = self.server.rpop(key)
            data = {
                'mid': mid,
                'pn': 1,
                'ps': 12,
                'sort': 'publish_time',
                'jsonp': 'jsonp'
            }
            url = self.start_urls[0] + urlencode(data)
            dict_1 = {'mid': mid}
            self.count_dict.setdefault(mid, 1)
            yield scrapy.FormRequest(url=url, callback=self.parse_article, meta=dict_1, headers=self.headers, dont_filter=True)

    def parse_article(self, response):
        mid = response.meta['mid']
        all_content = json.loads(response.text)
        item = BiliUserArticleItem()
        if 'data' in all_content.keys():
            if 'articles' in all_content['data'].keys():
                for content in all_content['data']['articles']:
                    item['article_id'] = content['id']  # 文章id
                    item['article_title'] = content['title']  # 文章标题
                    item['mid'] = content['author']['mid']  # 作者mid
                    item['author'] = content['author']['name']  # 作者name
                    item['view'] = content['stats']['view']  # 文章浏览
                    item['publish_time'] = content['publish_time']  # 文章发布时间
                    item['like'] = content['stats']['like']  # 文章点赞
                    item['reply'] = content['stats']['reply']  # 文章评论
                    item['share'] = content['stats']['share']  # 文章转发
                    yield item
                self.count_dict[mid] = self.count_dict[mid] + 1
                data = {
                    'mid': mid,
                    'pn':  self.count_dict[mid],
                    'ps': 12,
                    'sort': 'publish_time',
                    'jsonp': 'jsonp'
                }
                url = self.start_urls[0] + urlencode(data)
                dict_1 = {'mid': mid}
                yield scrapy.FormRequest(url=url, callback=self.parse_article, meta=dict_1, headers=self.headers, dont_filter=True)






