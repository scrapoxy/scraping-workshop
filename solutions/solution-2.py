from scrapy import Request, Spider
from scrapers.items import HotelItemLoader, ReviewItemLoader
from scrapers.utils import print_failure


class TrekkySpider(Spider):
    name = "trekky"

    start_url = "https://trekky-reviews.com/level2"

    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "Connection": "close",
            "Sec-Ch-Ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
        },

        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",

        "DOWNLOADER_MIDDLEWARES": {
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'scrapers.middlewares.retry.RetryMiddleware': 550,
        },
    }

    def start_requests(self):
        yield Request(
            url=self.start_url,
            callback=self.parse,
            errback=self.errback,
        )

    def parse(self, response):
        yield Request(
            url=response.urljoin("cities?city=paris"),
            callback=self.parse_hotels,
            errback=self.errback,
        )

    def parse_hotels(self, response):
        # Pagination
        for el in response.css('.pagination li a'):
            yield response.follow(
                url=el,
                callback=self.parse_hotels,
                errback=self.errback,
            )

        # Parse hotels
        for el in response.css('.hotel-link'):
            yield response.follow(
                url=el,
                callback=self.parse_hotel,
                errback=self.errback,
            )

    def parse_hotel(self, response):
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

    def errback(self, failure):
        print_failure(self.logger, failure)
