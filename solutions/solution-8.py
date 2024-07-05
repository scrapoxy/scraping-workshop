from base64 import b64encode
from scrapy import FormRequest, Request, Spider
from scrapers.items import HotelItemLoader, ReviewItemLoader
from scrapers.utils import print_failure
from urllib.parse import urljoin
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

import json


public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApgjwxZd4I6YnOE1GGCdnKIatX71CyGpssvAAH7udNLcBVr0WzIP1t+KZ7mDzLMyZE9MJmSsEgKidzaVRikarUQ6MUWnyJQxe8DlUNrSmK4ZrnLBD/5rVBcepZo1mPj1MdQWie4AYHUt++lLpPrXqEJ7xugSGIt7ORVGgcKO5ku5RSS1Ssy5iUhYtQo4VCb2UxYuMbpt2YF8LOaR8KtPIQENtNH2Jj7akQTna4I5lixOB0jme03lR5n94SqACUAZ+rFBDKgrC9eVWX8xdfMERxcKuD9NxFCV65tdNiH64CHWaDU13j9v2XGHKFkEORgRn+RQBintX5fEqt7GTTIzvoQIDAQAB"
pem_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
rsa_public_key = RSA.importKey(pem_key)
rsa_public_key = PKCS1_OAEP.new(rsa_public_key, hashAlgo=SHA256)

def rsa_encrypt(message):
    message = str.encode(message)
    encrypted_text = rsa_public_key.encrypt(message)
    encrypted_text_b64 = b64encode(encrypted_text)
    return encrypted_text_b64


class TrekkySpider(Spider):
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

    def build_payload(self):
        payload = json.dumps({
            "vendor": "Intel",
            "renderer": "Intel Iris OpenGL Engine",
        })
        payload_encoded = rsa_encrypt(payload)
        return payload_encoded

    def start_requests(self):
        yield Request(
            url=self.start_url,
            callback=self.parse_home,
            errback=self.errback,
        )

    def parse_home(self, response):
        yield FormRequest(
            url=urljoin(self.start_url, '/Vmi6869kJM7vS70sZKXrwn5Lq0CORjRl'),
            formdata={
                "payload": self.build_payload(),
            },
            callback=self.parse,
            errback=self.errback,
        )

    def parse(self, response):
        yield Request(
            url=self.start_url + "/cities?city=paris",
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

