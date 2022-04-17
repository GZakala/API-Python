import sys
sys.path.append('/home/george/Yandex.Disk/george/Lessons/homeworks/python/gb/api/lesson_7/') # Впишите сюда свой путь в lesson_7

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from furnitureparser.spiders.castorama import CastoramaSpider


if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(CastoramaSpider, query='стул')

    reactor.run()