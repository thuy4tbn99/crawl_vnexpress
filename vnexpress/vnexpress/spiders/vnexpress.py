import scrapy
from scrapy_splash import SplashRequest
from ..items import VnexpressItem
from scrapy_splash import SplashMiddleware
class VnexpressSpider(scrapy.Spider):
    name = 'vnexpress'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/thoi-su']

    def start_requests(self):
        print("hello\n\n")
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse_list_news, endpoint='render.html')
            # yield scrapy.Request(url=url, callback=self.parse_list_news)

    # def parse(self, response):
    #     for url in self.start_urls:
    #         print(url + '\n\n')
    #         yield scrapy.Request(url=url, callback=self.parse_list_news)    # get start_url and call parse_list func

    def parse_list_news(self, response):
        print("this is parse_list_news\n\n")
        list_news = response.css('.flexbox > div > .width_common a').css('::attr(href)').extract()   # get all link news from "thoi-su"

        for limit, news in enumerate(list_news):
            url = news
            print(url + '\n\n')
            if(url.startswith('https')):
            # yield scrapy.Request(url, callback=self.parse_news)
                yield SplashRequest(url=url, callback=self.parse_news, endpoint='render.html', args={'wait': 3})

    def parse_news(self, response):
        items = VnexpressItem()
        print( response.url + '\n\n')
        print(response.css('.nickname').css('::text').extract())
        items['category'] = response.css('.breadcrumb a').css('::attr(title)').extract()
        items['date'] = response.css('.date').css('::text').extract()
        items['title'] = response.css('.title-detail').css('::text').extract() 
        # items['category'] = response.css('.breadcrumb a').css('::attr(title)').extract()
        items['comment'] = response.css('.nickname').css('::text').extract()
        yield items



    # def start_requests(self):
    #     url = 'https://vnexpress.net/chu-tich-hoi-chu-thap-do-vn-thuy-tien-co-quyen-keu-goi-cuu-tro-4181040.html'
    #     # for url in self.start_urls:
    #     yield SplashRequest(url=url, callback=self.parse, endpoint='render.html')

    # def parse(self, response):
    #     items = VnexpressItem()
      
    #     items["date"] = response.css('.date').css('::text').extract()
    #     items["tags"] = response.css('.nickname').css('::text').extract()
    #     yield items




