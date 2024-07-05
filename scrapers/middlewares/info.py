from scrapy import signals

class InfoSpiderMiddleware:
    def __init__(self, stats):
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        s = cls(crawler.stats)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def spider_closed(self, spider):
        count = self.stats.get_value("item_scraped_count", 0, spider=spider)
        if count > 0:
            if count > 1:
                spider.logger.info(f"\n\nWe got: {count} items\n")
            else:
                spider.logger.info("\n\nWe got: 1 item\n")
