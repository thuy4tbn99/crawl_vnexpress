import scrapy
import re

from ..items import VnexpressItem
class VnexpressSpiderSpider(scrapy.Spider):
    name = 'vnexpress'
    allowed_domains = ['vnexpress.net']
    start_urls = ['http://vnexpress.net/thoi-su']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_list_news)

    def parse_list_news(self, response):
        print("this is parse_list_news\n\n")
        list_news = response.css('.width_common .title-news a').css('::attr(href)').extract()  
        for limit, url in enumerate(list_news):
            if(url.startswith('https://vnexpress.net/')):   # remove ads from link
                print(url)
                yield scrapy.Request(url=url, callback=self.parse_news) 
        
        # crawl next page 
        next_page =  response.css('.next-page::attr(href)').get()
        next_page = response.urljoin(next_page)
        page_number = int((re.findall('\d+', next_page))[0])
        print (next_page)
        if(next_page is not None and page_number <50):
            # pass
            print( ' with love \n\n')
            yield scrapy.Request(url=next_page, callback=self.parse_list_news)

    def parse_news(self, response):
        items = VnexpressItem()

        items['category'] = response.css('.breadcrumb a').css('::attr(title)').extract()
        items['date'] = response.css('.date').css('::text').extract()
        items['title'] = response.css('.title-detail').css('::text').extract()
        items["link"] = response.request.url
        print('here for items \n\n')
        items["user"] = response.css('.nickname').css('::attr(href)').extract()
        items['comment'] =''# response.css('#list_comment p:nth-child(1)').css('::text').extract()
        items['body'] = response.css('.top-detail p').css('::text').extract()

        yield items
