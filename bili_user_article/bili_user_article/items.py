# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BiliUserArticleItem(scrapy.Item):
    mid = scrapy.Field()
    author = scrapy.Field()
    publish_time = scrapy.Field()
    article_id = scrapy.Field()
    article_title = scrapy.Field()
    like = scrapy.Field()
    reply = scrapy.Field()
    view = scrapy.Field()
    share = scrapy.Field()
