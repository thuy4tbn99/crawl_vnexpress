# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VnexpressItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    category = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    comment = scrapy.Field()    
    user = scrapy.Field()   # list id user comment
    tags = scrapy.Field()   # haven't get
    link = scrapy.Field()
    id_user = scrapy.Field()    # used for cmt spider
    pass
