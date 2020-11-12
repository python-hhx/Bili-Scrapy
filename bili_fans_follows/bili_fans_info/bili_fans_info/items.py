# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BiliFansInfoItem(scrapy.Item):
    mid = scrapy.Field()
    fans_content = scrapy.Field()
    follows_content = scrapy.Field()
