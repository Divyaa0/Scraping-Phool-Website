import scrapy
from scrapy_splash import SplashRequest
import json



class SpySpider(scrapy.Spider):
    name = 'spy'
    # allowed_domains = ['abc']
    start_urls = ['https://phool.co/collections/']

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,
                                self.parse,
                                args={'wait': 0.5, 'viewport': '1024x2480', 'timeout': 90, 'images': 0,
                                      'resource_timeout': 10},
                                )

    def parse(self, response):
       an= response.css('.contains-children')[0]
       lis=an.css('li')
       link = lis.css('a::attr(href)').extract()


       for index, my_list in enumerate(link, start=1):
           if ( index >2 ):
                # category = link.css('a::text').extract()
                # yield {"list" : category}
               url=response.urljoin(my_list)
               yield scrapy.Request(url, callback=self.parse_contentzz)







    def parse_contentzz(self, response):

        card = response.css('div.product-info')
        title = response.css('nav.breadcrumb')






        for i in card:
            name = i.css('.title::text').extract()
            name=name[0]
            t_head = title.css('span::text').extract()
            t_head=t_head[0]

            rat = i.css('.jdgm-prev-badge__stars::attr(data-score)').extract()
            rat=float(rat[0])

            rev = i.css('.jdgm-prev-badge__text::text').extract()
            rev = rev[0]
            cleaned_rev=int(rev.replace('reviews' , '').replace('No', "0").replace('review',''))


            price = i.css('span.price::text').extract()
            price=price[0].strip()
            cleaned_price =float(price.replace('Rs.','').replace(",", ""))


            yield {"name": name,
                   "rating": rat,
                   "reviews": cleaned_rev,
                   "category":t_head,
                   "price": cleaned_price
                   }








