# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re
from hashlib import md5
from itemadapter import ItemAdapter
from bookparser.items import BookparserItem
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.mongobase = client['books']

    def process_item(self, item: BookparserItem, spider):
        if spider.name == 'labirint':
            insert_item = self.process_labirint(item)
        elif spider.name == 'book24':
            insert_item = self.process_book24(item)

        # Добавляем словарь в MongoDB
        collection = self.mongobase[spider.name]
        try:
            collection.insert_one(insert_item)
        except DuplicateKeyError:
            None

        return item

    def process_labirint(self, item: BookparserItem): 
        # Меняем значиния на числовые
        if item['price']:
            item['price'] = float( item['price'] )
        if item['discount_price']:
            item['discount_price'] = float( item['discount_price'] )
        if item['rating']:
            item['rating'] = float( item['rating'] )

        # Создаем словарь для генерации id через хэш функию
        item_dict = dict(item)
        # Генерируем id
        hash_id = md5(str(item_dict).encode('utf-8'))
        # Добавляем поле _id в словарь
        item['_id'] = hash_id.hexdigest()

        return item

    def process_book24(self, item: BookparserItem):
        # Меням значения на числовые
        if item['price']:
            item['price'] = re.sub(r' ', '', item['price'])
            item['price'] = float( re.search(r'[0-9]+', item['price'])[0] )
        if item['discount_price']:
            item['discount_price'] = re.sub(r' ', '', item['discount_price'])
            item['discount_price'] = float( re.search(r'[0-9]+', item['discount_price'])[0] )
        if item['rating']:
            item['rating'] = re.sub(r',', '.', item['rating'])
            item['rating'] = float( re.search(r'([0-9].[0-9]|[0-9])', item['rating'])[0] )
        
        # Создаем словарь для генерации id через хэш функию
        item_dict = dict(item)
        # Генерируем id
        hash_id = md5(str(item_dict).encode('utf-8'))
        # Добавляем поле _id в словарь
        item['_id'] = hash_id.hexdigest()

        return item