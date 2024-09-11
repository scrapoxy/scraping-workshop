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

    start_url = "https://trekky-reviews.com/level6"

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Connection": "close",
        },

        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'scrapers.middlewares.retry.RetryMiddleware': 550,
        },

        # Replace the default Scrapy downloader with Playwright and Chrome to manage JavaScript content.
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },

        # Set up Playwright to launch the browser in headful mode using Scrapoxy.
        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False,
            "proxy": {
                "server": "http://localhost:8888",
                "username": "TO_FILL",
                "password": "TO_FILL",
            },
        }
    }

    # Set up a global meta-configuration to use Playwright for every request.
    request_meta = dict(
        playwright=True,  # Enable Playwright
        playwright_include_page=True,  # Include the Playwright page object in the response
        playwright_context_kwargs=dict(
            ignore_https_errors=True,  # Ignore HTTPS errors
        ),
    )

    def start_requests(self):
        """This method initiates the web crawler's initial requests, starting by navigating to the website's
       homepage."""
        yield Request(
            url=self.start_url,
            callback=self.parse,
            errback=self.errback,
            meta=self.request_meta,
        )

    async def parse(self, response):
        """After accessing the website's homepage, we retrieve the list of hotels in Paris."""
        await response.meta["playwright_page"].close()

        # For the next requests, skip page rendering and download only the HTML content.
        self.request_meta["playwright_page_goto_kwargs"] = dict(
            wait_until='commit'
        )

        yield Request(
            url=response.urljoin("cities?city=paris"),
            callback=self.parse_hotels,
            errback=self.errback,
            meta=self.request_meta,
        )

    async def parse_hotels(self, response):
        """This method parses the list of hotels in Paris and also handles pagination."""
        await response.meta["playwright_page"].close()

        # Pagination
        for el in response.css('.pagination li a'):
            yield response.follow(
                url=el,
                callback=self.parse_hotels,
                errback=self.errback,
                meta={
                    **self.request_meta,
                }
            )

        # Hotel links
        for el in response.css('.hotel-link'):
            yield response.follow(
                url=el,
                callback=self.parse_hotel,
                errback=self.errback,
                meta={
                    **self.request_meta,
                }
            )

    async def parse_hotel(self, response):
        """This method parses hotel details such as name, email, and reviews."""
        await response.meta["playwright_page"].close()

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

    async def errback(self, failure):
        """This method handles and logs errors and is invoked with each request."""
        print_failure(self.logger, failure)
        await failure.request.meta["playwright_page"].close()
