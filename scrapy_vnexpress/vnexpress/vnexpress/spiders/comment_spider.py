import scrapy
import json
from ..items import CommentItem
class VnexpressSpiderSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['vnexpress.net']
    start_urls = []

    custom_settings = {
        'ITEM_PIPELINES': {'vnexpress.pipelines.CommentPipeline': 300,},    # setting used CommentPipeline
    }

    # formdata to make GET request to crawl comment
    articleID = ''
    siteID = ''
    categoryID = ''
    offset = '0'
    limit = '200'
    objecttype = '1'
    
    # get link article from csv
    def __init__(self):
        file_link = open('./link_article.csv', 'r+')
        for url in file_link.readlines():
            self.start_urls.append(url)

    def start_requests(self):
        for url in self.start_urls:
            print(url)
            yield scrapy.Request(url, callback=self.parse_metadata)
 
    # parse meta data and use FormRequest to send method Get to crawl comment of article
    def parse_metadata(self, response):
        self.articleID = response.css('meta[name="tt_article_id"]::attr(content)').extract()
        self.categoryID = response.css('meta[name="tt_category_id"]::attr(content)').extract()
        self.siteID = response.css('meta[name="tt_site_id"]::attr(content)').extract()
        # self.objecttype = response.css('meta[name="tt_page_type_new"]::attr(content)').extract()
        
        payload = {
            'objectid': self.articleID,
            'objecttype': self.objecttype,
            'siteid': self.siteID,
            'categoryid': self.categoryID,
            'offset': self.offset,
            'limit': self.limit
        }
        url = 'https://usi-saas.vnexpress.net/index/get'

        yield scrapy.FormRequest(url= url,callback= self.parse_comment, 
            method="GET", 
            formdata = payload,
        )
    
    # parse comment from article
    def parse_comment(self, response):
        items = CommentItem()

        response_data = json.loads(response.body)

        print(type(response_data['data']['total']))

        if(response_data['data']['total'] == 0):
            print("this is num ber = 0\n\n")
            items['total_comment'] = 0
        else:
            items['all_comment'] = response_data['data']['items']
            items['articleID'] = items['all_comment'][0]['article_id']
            items['userID'] = items['all_comment'][0]['userid']
            items['total_comment'] = response_data['data']['total']

        yield items
