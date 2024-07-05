from scrapy import Request, Spider
from scrapers.items import HotelItemLoader, ReviewItemLoader
from scrapers.utils import print_failure


class TrekkySpider(Spider):
    name = "trekky"

    start_url = "https://trekky-reviews.com/level7"

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Connection": "close",
        },

        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },

        "PLAYWRIGHT_LAUNCH_OPTIONS": {
            "headless": False,
            "proxy": {
                "server": "http://localhost:8888",
                "username": "TO_FILL",
                "password": "TO_FILL",
            },
        }
    }

    request_meta = dict(
        playwright=True,
        playwright_include_page=True,
        playwright_context_kwargs=dict(
            ignore_https_errors=True,
            timezone_id='America/Chicago',
        ),
    )

    def start_requests(self):
        yield Request(
            url=self.start_url,
            callback=self.parse,
            errback=self.errback,
            meta=self.request_meta,
        )

    async def parse(self, response):
        await response.meta["playwright_page"].close()

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

        # Hotels
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
        await response.meta["playwright_page"].close()

        reviews = [self.get_review(review_el) for review_el in response.css('.hotel-review')]

        hotel = HotelItemLoader(response=response)
        hotel.add_css('name', '.hotel-name::text')
        hotel.add_css('email', '.hotel-email::text')
        hotel.add_value('reviews', reviews)
        return hotel.load_item()

    def get_review(self, review_el):
        review = ReviewItemLoader(selector=review_el)
        review.add_css('rating', '.review-rating::text')
        return review.load_item()

    async def errback(self, failure):
        print_failure(self.logger, failure)
        await failure.request.meta["playwright_page"].close()
