import scrapy
from scrapy_splash import SplashRequest
from ..items import VnexpressItem
from scrapy_splash import SplashMiddleware
class VnexpressSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/nhung-ngu-dan-khong-ngoi-yen-trong-lu-4179643.html']


    script = """
        function main(splash)
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(0.5))       
            return {
                html = splash:html(),
                url = splash:url(),
            }
        end
        """

    def parse(self, response):
        print("hello")
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse_news, endpoint='render.html')

    def parse_news(self, response):
        items = VnexpressItem()
      
        items["date"] = response.css('.date').css('::text').extract()
        items["tags"] = response.css('.nickname').css('::text').extract()
        yield items
        
        # yield SplashRequest(
        #     url=response.url,
        #     callback=self.parse,
        #     meta={
        #         "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
        #     },
        # )  



