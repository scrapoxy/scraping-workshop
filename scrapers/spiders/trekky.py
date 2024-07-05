from scrapy import Request, Spider
from scrapers.items import HotelItemLoader, ReviewItemLoader
from scrapers.utils import print_failure


class TrekkySpider(Spider):
    # The unique name of the spider
    name = "trekky"

    # Root of the website and first URL to scrape
    start_url = "TO_FILL"

    # Custom settings for the scraper
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Connection": "close",
        },

        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'scrapers.middlewares.retry.RetryMiddleware': 550,
        },
    }

    # This function initiates the first requests of the web crawler.
    # Here, we navigate to the root of the website.
    def start_requests(self):
        yield Request(
            url=self.start_url,
            callback=self.parse,
            errback=self.errback,
        )

    # This function processes the response from the previous request and initiates a new one.
    # Here, we retrieve the list of accommodations in Paris.
    def parse(self, response):
        pass  # TO_FILL

    # This function parses a list of accommodations.
    # It iterates through the list of accommodations and manages pagination as well.
    def parse_hotels(self, response):
        # Pagination
        pass  # TO_FILL

        # Parse hotels
        pass  # TO_FILL

    # This function parses accommodation details such as name, email, and reviews.
    def parse_hotel(self, response):
        pass  # TO_FILL

    # This function extracts rating from a review
    def get_review(self, review_el):
        review = ReviewItemLoader(selector=review_el)
        review.add_css('rating', '.review-rating::text')
        return review.load_item()

    # This function handles and prints errors and needs to be invoked for every request
    def errback(self, failure):
        print_failure(self.logger, failure)
