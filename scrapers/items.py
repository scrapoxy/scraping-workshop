from dataclasses import dataclass, field
from itemloaders.processors import TakeFirst, MapCompose, Identity
from scrapy.loader import ItemLoader


@dataclass
class ReviewItem:
    rating: float = field(default=None)


class ReviewItemLoader(ItemLoader):
    default_item_class = ReviewItem
    rating_in = MapCompose(str.strip, float)
    rating_out = TakeFirst()


@dataclass
class HotelItem:
    name: str = field(default=None)
    email: str = field(default=None)
    reviews: list[ReviewItem] = field(default=None)


class HotelItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    default_item_class = HotelItem

    reviews_in = Identity()
    reviews_out = Identity()

