import re
import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    page=1
    start_urls = ['https://book24.ru/search/page-1/?q=игры']

    def parse(self, response: HtmlResponse):
        if response.status == 404:
            return None
        
        next_page = re.sub(r'page-' + str(self.page), 'page-' + str(self.page + 1), response.url)
        self.page += 1
        yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//article[@class="product-card"]/div[2]/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_book)
        
    def parse_book(self, response: HtmlResponse):
        link = response.url
        name = response.xpath('//h1[@itemprop="name"]/text()').get()
        authors = response.xpath('//ul[@class="product-characteristic__list"]/li/div/div[2]/a/text()').get()
        price = response.xpath('//div[contains(@class, "product-sidebar")]//div[contains(@class, "product-sidebar-price")]//span/text()').get()
        discount_price = response.xpath('//div[contains(@class, "product-sidebar")]//div[contains(@class, "product-sidebar-price")]//div[@itemprop="offers"]//span/text()').get()
        rating = response.xpath('//button[@class="rating-widget__button"]/span[2]/text()').get()
        
        yield BookparserItem(
            link=link,
            name=name,
            authors=authors,
            price=price,
            discount_price=discount_price,
            rating=rating
        )