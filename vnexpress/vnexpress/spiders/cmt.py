import scrapy
import re
from scrapy_splash import SplashRequest
from ..items import VnexpressItem
from scrapy_splash import SplashMiddleware
class VnexpressSpider(scrapy.Spider):
    name = 'cmt'
    # allowed_domains = ['vnexpress.net']
    start_urls = ['https://my.vnexpress.net/users/feed/1049321585']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse,
                args={'wait': 0.5}
            )
    script = """
    function main(splash)
    local url = splash.args.url -- splash.args.url
    assert(splash:go(url))
    assert(splash:wait(0.5))
    for i=1,5 do
        print(i)
        assert(splash:runjs("$('#load_more_comment').click()"))
        splash:wait(3)
    end
    return {
        html = splash:html(),
        png = splash:png(),
    }
    end
    """

    def parse(self, response):
        items = VnexpressItem()
        
        items["comment"] = response.css('.width_common .content_com p').css('::text').extract()
        yield items
        
        print("continue\n\n")
        for i in range(1,5):
            yield SplashRequest(
                url=response.url,
                callback=self.parse,
                # dont_filter = True,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )




