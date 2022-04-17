# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def convert_price(price: str):
    price = price.replace('\xa0', '').replace(' ', '')
    try:
        price = int(price)
    except Exception:
        return price
    return price


class FurnitureparserItem(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(convert_price), output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    characteristics = scrapy.Field()
    _id = scrapy.Field()
