from itemadapter import ItemAdapter
from scrapy import signals

import csv


class SaveToCsvPipeline:
    ###This pipeline class saves the scraped data to a CSV file named 'results.csv'.###
    _items = []

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def process_item(self, item, spider):
        self._items.append(item)
        return item

    def spider_opened(self, spider):
        self._items = []

    def spider_closed(self, spider):
        with open('results.csv', 'w', newline='') as csvfile:
            csvwriter = csv.DictWriter(
                csvfile,
                fieldnames=['name', 'email', 'reviews'],
                delimiter=',',
                quotechar='"', quoting=csv.QUOTE_MINIMAL
            )

            csvwriter.writeheader()

            for item in self._items:
                csvwriter.writerow(ItemAdapter(item).asdict())
