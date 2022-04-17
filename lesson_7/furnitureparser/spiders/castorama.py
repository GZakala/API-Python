import sys
sys.path.append('/home/george/Yandex.Disk/george/Lessons/homeworks/python/gb/api/lesson_7/') # Впишите сюда свой путь в leroyparser

import scrapy
from scrapy.http import HtmlResponse
from furnitureparser.items import FurnitureparserItem
from scrapy.loader import ItemLoader


class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.query = input('Что вы хотите найти?: ') # Это значение будет использоваться, как название коллекции
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={self.query}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class="next i-next"]')
        if next_page:
            yield response.follow(next_page[0], callback=self.parse)

        links = response.xpath('//a[contains(@class, "product-card__name")]/@href')
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=FurnitureparserItem(), response=response)
        loader.add_xpath('title', '//h1[@itemprop="name"]/text()')
        loader.add_xpath('photos', '//li[contains(@class, "top-slide")]/div/img[last()]/@data-src')
        loader.add_xpath('price', '//span[@class="price"]/span/span[1]/text()')
        loader.add_value('link', response.url)
        loader.add_xpath('characteristics', '//div[@id="specifications"]/dl/*[contains(@class, "specs-table__attribute")]//text()')
        yield loader.load_item()
