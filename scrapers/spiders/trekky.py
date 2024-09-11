from scrapy import Request, Spider
from scrapers.items import HotelItemLoader, ReviewItemLoader
from scrapers.utils import print_failure


class TrekkySpider(Spider):
    """This class manages all the logic required for scraping the Trekky website.

    Attributes:
        name (str): The unique name of the spider.
        start_url (str): Root of the website and first URL to scrape.
        custom_settings (dict): Custom settings for the scraper
    """

    name = "trekky"

    start_url = "https://trekky-reviews.com/level1"

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Connection": "close",
        },

        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'scrapers.middlewares.retry.RetryMiddleware': 550,
        },
    }

    def start_requests(self):
        """This method initiates the web crawler's initial requests, starting by navigating to the website's
        homepage."""
        yield Request(
            url=self.start_url,
            callback=self.parse,
            errback=self.errback,
        )

    def parse(self, response):
        """After accessing the website's homepage, we retrieve the list of hotels in Paris."""
        yield Request(
            url=response.urljoin("cities?city=paris"),
            callback=self.parse_hotels,
            errback=self.errback,
        )

    def parse_hotels(self, response):
        """This method parses the list of hotels in Paris and also handles pagination."""

        # Pagination
        for el in response.css('.pagination li a'):
            yield response.follow(
                url=el,
                callback=self.parse_hotels,
                errback=self.errback,
            )

        # Hotel links
        for el in response.css('.hotel-link'):
            yield response.follow(
                url=el,
                callback=self.parse_hotel,
                errback=self.errback,
            )

    def parse_hotel(self, response):
        """This method parses hotel details such as name, email, and reviews."""
        reviews = [self.get_review(review_el) for review_el in response.css('.hotel-review')]

        hotel = HotelItemLoader(response=response)
        hotel.add_css('name', '.hotel-name::text')
        hotel.add_css('email', '.hotel-email::text')
        hotel.add_value('reviews', reviews)
        return hotel.load_item()

    def get_review(self, review_el):
        """This method extracts rating from a review"""
        review = ReviewItemLoader(selector=review_el)
        review.add_css('rating', '.review-rating::text')
        return review.load_item()

    def errback(self, failure):
        """This method handles and logs errors and is invoked with each request."""
        print_failure(self.logger, failure)
