import scrapy
import json
import re
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
            if(id == '\n'):
                continue
                print('\n \n is break')
            url = 'https://usi-saas.vnexpress.net/api/comment/bytime'
            payload ={
                'user_id': id,
                'offset': '0',
                'limit': '5000',
            }

            yield scrapy.FormRequest(url= url,callback= self.parse_user, 
                method="GET", 
                formdata = payload,
            )
    
    def parse_user(self, response):
        items = UserItem()

        response_data = json.loads(response.body) # list of comment in json format
        len_response = len(response_data)

        
        # items['comment'] = response_data
        
        # get data response (json format) and convert to list
        timeList = []
        contentList = []
        linkList = []
        for idx in range(len_response):
            time = response_data[idx]['time']
            content = response_data[idx]['content']
            link = response_data[idx]['url']
            # print(time, content, link)

            timeList.append(time)
            contentList.append(content)
            linkList.append(link)
        
        userId = response_data[0]['userid']
        

        if(not userId or not timeList or not contentList or not linkList):
            yield
        else:
            items['userID'] = userId
            items['time'] = timeList
            items['comment'] = contentList
            items['url'] = linkList
            yield items

        # handle each comment of each user
        # for idx_comment in range(len_response):
        #     items['userID'] = response_data[idx_comment]['userid']
        #     items['url'] = response_data[idx_comment]['url']
        #     items['comment'] = response_data[idx_comment]['content']
        #     items['articleID'] = response_data[idx_comment]['article_id']
        #     items['categoryID'] = response_data[idx_comment]['category_id']
        #     items['time'] = response_data[idx_comment]['time']
