import scrapy
import re
from scrapy_splash import SplashRequest
from ..items import VnexpressItem
from scrapy_splash import SplashMiddleware
class VnexpressSpider(scrapy.Spider):
    name = 'vnexpress'
    allowed_domains = ['vnexpress.net']
    start_urls = ['https://vnexpress.net/thoi-su']

    debug = False

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url=url, callback=self.parse_list_news,     # used splash request instead scrapy request but used scrapy.Request is oke but not crawl all cmt st have error
                args={'wait': 0.5}
            )

    # get link from 'thoi-su' and pass to par
    def parse_list_news(self, response):
        print("this is parse_list_news\n\n")
        list_news = response.css('.width_common .title-news a').css('::attr(href)').extract()  
        for limit, url in enumerate(list_news):
            if(url.startswith('https://vnexpress.net/')):   # remove ads from link
                print(url)
                yield SplashRequest(url=url, callback=self.parse_news, 
                    endpoint='render.html', 
                    meta={'original_url': url},          # meta keep orginial link, if not show only endpoint link
                    args={'wait': 0.5},
                ) 
        # crawl next page 
        next_page =  response.css('.next-page::attr(href)').get()
        next_page = response.urljoin(next_page)
        page_number = int(re.findall('([a-z]+)(\d+)', next_page)[0][1])
        print (next_page)
        if(next_page is not None and page_number <50):
            # pass
            print( ' with love \n\n')
            yield SplashRequest(url=next_page, callback=self.parse_list_news,
                endpoint='render.html',
                args={'wait': 0.5},
            )

    # lua script to get more comment and next page comment
    script ="""
        function main(splash)
        local url = splash.args.url -- splash.args.url
        assert(splash:go(url))
        assert(splash:wait(0.5))
        assert(splash:runjs("$('.view_more_coment a').click()"))    -- click button more comment
        return {
            --html = splash:html(),
            --png = splash:png(),
        }
        end
    """

    # get response and pass to items
    def parse_news(self, response):
        items = VnexpressItem()
        
        try:
            original_url = response.meta['original_url']
        except KeyError:
            original_url = 'None'
            self.debug = True
        print('thuy\n\n' + original_url + '\t' +str(self.debug))

        if self.debug:
            self.debug = False
            pass
        else:
            yield SplashRequest(
                url=response.url,
                callback=self.parse_news,
                meta={
                    "splash": {"endpoint": "execute", "args": {"lua_source": self.script}}
                },
            )

            items['category'] = response.css('.breadcrumb a').css('::attr(title)').extract()
            items['date'] = response.css('.date').css('::text').extract()
            items['title'] = response.css('.title-detail').css('::text').extract()
            items["link"] = original_url
            print('here for items \n\n')
            items["user"] = response.css('.nickname').css('::attr(href)').extract()
            items['comment'] = response.css('#list_comment p:nth-child(1)').css('::text').extract()
            items['body'] = response.css('.top-detail p').css('::text').extract()
            yield items

            






