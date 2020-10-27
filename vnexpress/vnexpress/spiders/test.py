import scrapy
from scrapy_splash import SplashRequest
from scrapy_splash import SplashResponse
from ..items import VnexpressItem
from scrapy_splash import SplashMiddleware
class VnexpressSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/le-tang-22-quan-nhan-bi-vui-lap-4180308-tong-thuat.html']


    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse_news,     # used splash request instead scrapy request
                args={'wait': 0.5},
                endpoint= 'render.html',
                meta ={'original_url': url}
            )

    
    # def parse_list_news(self, response):
    #     list_news = response.css('.width_common .title-news a').css('::attr(href)').extract()   #get list_news from thoisu
    #     for limit, url in enumerate(list_news):
    #         if(url.startswith('https://vnexpress.net/')):
    #             print(url)
    #             self.link =  url
    #             yield SplashRequest(url=url, callback=self.parse_news, endpoint='render.html', meta={'original_url': url})
        
    #     next_page =  response.css('.next-page::attr(href)').get()
    #     next_page = response.urljoin(next_page)
    #     print (next_page)
    #     if(next_page is not None):
    #         pass
    #         yield SplashRequest(url=next_page, callback=self.parse_list_news,
    #             # endpoint='render.html',
    #             args={'wait': 0.5},
    #         )
        # print(next_page)
    
    script ="""
        function main(splash)
        local url = splash.args.url -- splash.args.url
        print(url)
        assert(splash:go(url))
        assert(splash:wait(0.5))
        assert(splash:runjs("$('.view_more_coment a').click()"))    -- click button more comment
        for i=1,5 do
            print(i)
            assert(splash:runjs("$('#pagination > div > a.btn-page.next-page').click()"))   -- click get next-page comment
            splash:wait(0.5)
        end
        return {
            html = splash:html(),
            png = splash:png(),
        }
        end
    """

    def parse_news(self, response):
        items = VnexpressItem()   

        # items["link"] = response.meta['original_url']
        items['comment'] = response.css('#list_comment p:nth-child(1)').css('::text').extract()
        yield items
        
        yield SplashRequest(
            url=response.url,
            callback=self.parse_news,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )



