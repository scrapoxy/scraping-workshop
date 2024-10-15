from scrapy import FormRequest, Request, Spider
from scrapers.items import HotelItemLoader, ReviewItemLoader
from scrapers.utils import print_failure, rsa_encrypt
from urllib.parse import urljoin

import json


def build_payload():
    """Build the encrypted payload to send to the server."""
    payload = json.dumps({
        "vendor": "Intel",
        "renderer": "Intel Iris OpenGL Engine",
    })

    # The public key is extracted from the deobfuscated JavaScript code of the website's antibot.
    public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApgjwxZd4I6YnOE1GGCdnKIatX71CyGpssvAAH7udNLcBVr0WzIP1t+KZ7mDzLMyZE9MJmSsEgKidzaVRikarUQ6MUWnyJQxe8DlUNrSmK4ZrnLBD/5rVBcepZo1mPj1MdQWie4AYHUt++lLpPrXqEJ7xugSGIt7ORVGgcKO5ku5RSS1Ssy5iUhYtQo4VCb2UxYuMbpt2YF8LOaR8KtPIQENtNH2Jj7akQTna4I5lixOB0jme03lR5n94SqACUAZ+rFBDKgrC9eVWX8xdfMERxcKuD9NxFCV65tdNiH64CHWaDU13j9v2XGHKFkEORgRn+RQBintX5fEqt7GTTIzvoQIDAQAB"

    payload_encoded = rsa_encrypt(payload, public_key)
    return payload_encoded


class TrekkySpider(Spider):
    """This class manages all the logic required for scraping the Trekky website.

    Attributes:
        name (str): The unique name of the spider.
        start_url (str): Root of the website and first URL to scrape.
        custom_settings (dict): Custom settings for the scraper
    """

    name = "trekky"

    start_url = "https://trekky-reviews.com/level8"

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
        """This method start 10 separate sessions on the homepage, one per page."""
        for page in range(1, 10):
            yield Request(
                url=self.start_url,
                callback=self.parse_home,
                errback=self.errback,
                dont_filter=True,
                meta=dict(
                    page=page,
                    cookiejar="jar%d" % page,
                ),
            )

    def parse_home(self, response):
        """After accessing the website's homepage, we generate the encrypted payload and send it to the server."""
        yield FormRequest(
            url=urljoin(self.start_url, '/Vmi6869kJM7vS70sZKXrwn5Lq0CORjRl'),
            formdata={
                "payload": build_payload(),
            },
            callback=self.parse,
            errback=self.errback,
            dont_filter=True,
            meta=response.meta,
        )

    def parse(self, response):
        """Once approved, we retrieve the list of hotels in Paris from page X."""
        yield Request(
            url=self.start_url + "/cities?city=paris&page=%d" % response.meta['page'],
            callback=self.parse_listing,
            errback=self.errback,
            meta=response.meta,
        )

    def parse_listing(self, response):
        """This method parses the list of hotels in Paris from page X."""
        for el in response.css('.hotel-link'):
            yield response.follow(
                url=el,
                callback=self.parse_hotel,
                errback=self.errback,
                meta=response.meta,
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

