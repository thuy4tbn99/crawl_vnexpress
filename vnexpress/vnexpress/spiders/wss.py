# -*- coding: utf-8 -*-
import scrapy
from ..items import VnexpressItem
from scrapy_splash import SplashRequest

class WebsosanhSpider(scrapy.Spider):

    name = "wss"
    allowed_domains = ['websosanh.vn']
    start_urls = ["https://websosanh.vn/dan-organ/cat-2022.htm"]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, endpoint="render.html", callback=self.parse)

    script = """
        function main(splash)
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(0.5))
            assert(splash:runjs("$('.next')[0].click();"))
            return {
                html = splash:html(),
                url = splash:url(),
            }
        end
        """

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, endpoint="render.html", callback=self.parse)

    def parse(self, response):
        item = VnexpressItem()
        for data in response.xpath("//li[@class='item ']"):
            item["name"] = data.xpath("./h3/a/text()").extract_first()
            if item["name"] == None:
                item["name"] = data.xpath("./h2/a/text()").extract_first()
            item["price"] = data.xpath("./div[2]/text()").extract_first()
            item["image"] = data.xpath("./div[1]/a/img[1]/@data-src").extract_first()
            yield item

        yield SplashRequest(
            url=response.url,
            callback=self.parse,
            meta={
                "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
            },
        )