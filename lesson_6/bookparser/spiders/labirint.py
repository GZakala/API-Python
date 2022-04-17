import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/игры/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//div[@class="pagination-next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        
        links = response.xpath('//a[@class="product-title-link"]/@href')
        for link in links:
            yield response.follow(link, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):
        link = response.url
        name = response.xpath('//div[@id="product-title"]/h1/text()').get()
        authors = response.xpath('//div[@class="authors"]/a/text()').get()
        price = response.xpath('//div[@class="buying-priceold-val"]/span/text()').get()
        discount_price = response.xpath('//div[@class="buying-pricenew-val"]/span/text()').get()
        rating = response.xpath('//div[@id="rate"]/text()').get()
        
        yield BookparserItem(
            link=link,
            name=name,
            authors=authors,
            price=price,
            discount_price=discount_price,
            rating=rating
        )

