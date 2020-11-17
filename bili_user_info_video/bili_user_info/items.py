# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BiliUserInfoItem(scrapy.Item):
    mid = scrapy.Field()
    name = scrapy.Field()
    sex = scrapy.Field()
    birthday = scrapy.Field()
    sign = scrapy.Field()
    all_video_info = scrapy.Field()
    all_dynamic = scrapy.Field()
    all_video_type = scrapy.Field()
    test_id = scrapy.Field()


