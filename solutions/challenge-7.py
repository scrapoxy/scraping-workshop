#!/usr/bin/env python3
from dataclasses import dataclass, field
from parsel import Selector
from camoufox.async_api import AsyncCamoufox
from typing import List, Iterator
from urllib.parse import urljoin

import asyncio
import csv
import logging


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


# Define data classes similar to those in scrapers/items.py
@dataclass
class ReviewItem:
    rating: float = field(default=None)


@dataclass
class HotelItem:
    name: str = field(default=None)
    email: str = field(default=None)
    reviews: List[ReviewItem] = field(default_factory=list)


class TrekkyCamoufoxSpider:
    """Pure Camoufox implementation of the Trekky spider."""
    start_url = "https://trekky-reviews.com/level9"

    logger = logging.getLogger(__name__)

    async def start(self) -> None:
        """Entry point to start the scraping process."""
        if not self.start_url.endswith('/'):
            self.start_url += '/'

        tasks = []
        # Create separate sessions
        for page_num in range(1, 10):
            task = asyncio.create_task(self.parse_homepage(page_num))
            tasks.append(task)

        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Process results
        hotels = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"Error occurred: {result}")
            elif result:
                hotels.extend(result)

        # Output results to a CSV file matching the required format
        with open('../results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'email', 'reviews'])
            for hotel in hotels:
                reviews_str = str([{"rating": review.rating} for review in hotel.reviews])
                writer.writerow([hotel.name, hotel.email, reviews_str])

        self.logger.info(f"Scraped {len(hotels)} hotels and saved to results.csv")

    async def parse_homepage(self, page_num) -> List[HotelItem]:
        """This method starts a session for the homepage and retrieves the list of hotels in Paris from page X."""
        hotels = []

        try:
            # Launch browser with camoufox
            async with AsyncCamoufox(
                headless=False,
            ) as browser:
                # Create a new context
                context = await browser.new_context(
                    ignore_https_errors=True,
                )

                # Open a new page and navigate to the homepage
                self.logger.info(f"Go to homepage for page {page_num}")

                page = await context.new_page()
                await page.route('**/*.{png,jpg,jpeg,svg,gif,css}', lambda route: route.abort())
                await page.goto(self.start_url, wait_until='networkidle', timeout=60000)
                await page.wait_for_timeout(2000)

                # Navigate to the listing page and get the hotels
                url = urljoin(self.start_url, f"cities?city=paris&page={page_num}")
                async for hotel in self.parse_listing(page, url):
                    hotels.append(hotel)

                # Close the page and context
                await page.close()
                await context.close()

        except Exception as e:
            self.logger.error(f"Error in session {page_num}: {e}")
            raise

        return hotels

    async def parse_listing(self, page, url) -> Iterator[HotelItem]:
        """This method parses the list of hotels."""
        self.logger.info(f"Go to listing page: {url}")
        await page.goto(url, wait_until='networkidle', timeout=60000)

        # Wait longer for JavaScript to load content
        await page.wait_for_timeout(5000)

        selector = Selector(text=await page.content())

        for link in selector.css('.hotel-link'):
            href = link.attrib.get('href')
            if href:
                hotel_url = urljoin(self.start_url, href)

                try:
                    item = await self.parse_hotel(page, hotel_url)
                    if item:
                        yield item
                except Exception as e:
                    self.logger.error(f"Error scraping hotel {hotel_url}: {e}")

    async def parse_hotel(self, page, url) -> HotelItem | None:
        """This method parses hotel details."""
        try:
            self.logger.info(f"Go to hotel page: {url}")
            await page.goto(url, wait_until='commit', timeout=30000)
            await page.wait_for_selector('.hotel-name', timeout=10000)

            selector = Selector(text=await page.content())

            reviews = []
            for review_el in selector.css('.hotel-review'):
                review_item = self.get_review(review_el)
                if review_item:
                    reviews.append(review_item)

            name = selector.css('.hotel-name::text').get()
            email = selector.css('.hotel-email::text').get()

            if name and email:
                return HotelItem(name=name.strip(), email=email.strip(), reviews=reviews)
            else:
                self.logger.warning(f"Incomplete hotel data extracted: name={name}, email={email}")
                return None

        except Exception as e:
            self.logger.error(f"Error extracting hotel info: {e}")
            return None

    def get_review(self, review_el) -> ReviewItem | None:
        """This method extracts rating from a review"""
        rating_text = review_el.css('.review-rating::text').get()
        try:
            rating = float(rating_text.strip()) if rating_text else None
            return ReviewItem(rating=rating)
        except (ValueError, TypeError):
            self.logger.warning(f"Invalid rating value: {rating_text}")
            return None




async def main():
    """Main entry point."""
    spider = TrekkyCamoufoxSpider()
    await spider.start()


if __name__ == "__main__":
    asyncio.run(main())
