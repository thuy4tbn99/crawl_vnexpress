import scrapy
import json
from ..items import UserItem
class VnexpressSpiderSpider(scrapy.Spider):
    name = 'user'
    allowed_domains = ['vnexpress.net']
    start_urls = []

    custom_settings = {
        'ITEM_PIPELINES': {'vnexpress.pipelines.UserPipeline': 300,},    # setting used UserPipeline
    }

    def start_requests(self):
        userIDs = open('./userID.csv', 'r+')

        for id in userIDs.readlines():
            url = 'https://usi-saas.vnexpress.net/api/comment/bytime'
            payload ={
                'user_id': id,
                'offset': '0',
                'limit': '20',
            }

            yield scrapy.FormRequest(url= url,callback= self.parse_user, 
                method="GET", 
                formdata = payload,
            )
    
    def parse_user(self, response):
        items = UserItem()

        response_data = json.loads(response.body) # list of comment in json format
        len_response = len(response_data)
        for idx_comment in range(len_response):
            items['userID'] = response_data[idx_comment]['userid']
            items['url'] = response_data[idx_comment]['url']
            items['comment'] = response_data[idx_comment]['content']
            items['articleID'] = response_data[idx_comment]['article_id']
            items['categoryID'] = response_data[idx_comment]['category_id']
            yield items
