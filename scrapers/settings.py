BOT_NAME = "scrapers"

SPIDER_MODULES = ["scrapers.spiders"]
NEWSPIDER_MODULE = "scrapers.spiders"

CONCURRENT_REQUESTS = 5
DOWNLOAD_TIMEOUT = 10

SPIDER_MIDDLEWARES = {
    'scrapers.middlewares.info.InfoSpiderMiddleware': 40,
}

ITEM_PIPELINES = {
    'scrapers.pipelines.csv.SaveToCsvPipeline': 300,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

# Prevent Scrapy from overriding Chrome's default HTTP headers.
PLAYWRIGHT_PROCESS_REQUEST_HEADERS=None
