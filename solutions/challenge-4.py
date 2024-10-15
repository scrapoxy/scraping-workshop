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

    # No changes are needed for this challenge compared to the previous one, as all adjustments were made in Scrapoxy.
    start_url = "https://trekky-reviews.com/level4"

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",

        "DEFAULT_REQUEST_HEADERS": {
            "Connection": "close",
            "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
        },

        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'scrapers.middlewares.retry.RetryMiddleware': 550,
            'scrapoxy.ProxyDownloaderMiddleware': 100,
        },

        "SCRAPOXY_MASTER": "http://localhost:8888",
        "SCRAPOXY_API": "http://localhost:8890/api",
        "SCRAPOXY_USERNAME": "TO_FILL",
        "SCRAPOXY_PASSWORD": "TO_FILL",
    }

    def start_requests(self):
        """This method start 10 separate sessions on the homepage, one per page."""
        for page in range(1, 10):
            yield Request(
                url=self.start_url,
                callback=self.parse,
                errback=self.errback,
                dont_filter=True,
                meta=dict(
                    page=page,
                    cookiejar="jar%d" % page,
                ),
            )

    def parse(self, response):
        """After accessing the website's homepage, we retrieve the list of hotels in Paris from page X."""
        yield Request(
            url=response.urljoin("cities?city=paris&page=%d" % response.meta['page']),
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
