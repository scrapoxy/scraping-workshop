from datetime import datetime
from scrapy.spidermiddlewares.httperror import HttpError
from w3lib.html import remove_tags

import re
import json


def remove_whitespace(text):
    text = text.replace('\n', ' ').replace('\r', '')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def date_to_timestamp(date):
    try:
        return int(datetime.strptime(date.strip(), '%b %d, %Y, %I:%M %p').timestamp() * 1000)
    except ValueError:
        return None


def print_failure(logger, failure):
    message = f"\nURL: {failure.request.url}\n\n"

    if failure.check(HttpError):
        response = failure.value.response

        text = remove_tags(response.text)

        try:
            if response.status == 429:
                error = {
                    "message": "Too many requests",
                    "description": response.text
                }
            else:
                error = json.loads(text)

            message += f"Error: {error['message']}\n\nDetails: {error['description']}\n"
        except json.JSONDecodeError:
            message += text
    else:
        message += f"Error: {failure.getErrorMessage()}\n"

    logger.error(f"\n{message}\n")
