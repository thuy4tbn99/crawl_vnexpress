import scrapy
from scrapy_splash import SplashRequest
from scrapy_splash import SplashResponse
from ..items import VnexpressItem
from scrapy_splash import SplashMiddleware
class VnexpressSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/thoi-su']

    # script = """
    #     function main(splash)
    #         local url = splash.args.url
    #         assert(splash:go(url))
    #         assert(splash:wait(0.5))       
    #         return {
    #             html = splash:html(),
    #             url = splash:url(),
    #         }
    #     end
    #     """

    def parse(self, response):
        print("hello")
        for url in self.start_urls:
            yield SplashRequest(url, self.parse_list_news,#dont_process_response=True,
                # endpoint='render.html',
                args={'wait': 0.5},
            )
            # yield SplashRequest(url, dont_process_response=True, args={'wait': 10}, meta={'real_url': url})
    
    def parse_list_news(self, response):
        list_news = response.css('.width_common .title-news a').css('::attr(href)').extract()   #get list_news from thoisu
        for limit, url in enumerate(list_news):
            if(url.startswith('https://vnexpress.net/')):
                print(url)
                self.link =  url
                yield SplashRequest(url=url, callback=self.parse_news, endpoint='render.html', meta={'original_url': url})
        
        next_page =  response.css('.next-page::attr(href)').get()
        next_page = response.urljoin(next_page)
        page_number = int(re.findall('([a-z]+)(\d+)', next_page)[0][1])
        print (next_page)
        if(next_page is not None and page_number <30):
            yield SplashRequest(url=next_page, callback=self.parse_list_news,
                # endpoint='render.html',
                args={'wait': 0.5},
            )
        

    def parse_news(self, response):
        items = VnexpressItem()   #test items is global or local
        items["link"] = response.meta['original_url']
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



