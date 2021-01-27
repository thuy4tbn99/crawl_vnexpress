# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VnexpressItem(scrapy.Item):
    # define the fields for your item here like:

    category = scrapy.Field()
    date = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    
    categoryID = scrapy.Field()    
    siteID = scrapy.Field()  
    articleID = scrapy.Field()   
    link = scrapy.Field()
    tags = scrapy.Field()   # haven't get
    pass

class CommentItem(scrapy.Item):
    userID = scrapy.Field()
    articleID = scrapy.Field()
    all_comment = scrapy.Field()
    total_comment = scrapy.Field()
    pass

class UserItem(scrapy.Item):
    userID = scrapy.Field()
    comment = scrapy.Field()
    url = scrapy.Field()
    categoryID = scrapy.Field()
    articleID = scrapy.Field()
    time = scrapy.Field() 
    pass
