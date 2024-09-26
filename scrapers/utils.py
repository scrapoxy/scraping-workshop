from base64 import b64encode
from datetime import datetime
from scrapy.spidermiddlewares.httperror import HttpError
from w3lib.html import remove_tags
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

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


def rsa_encrypt(message, public_key):
    """Use RSA public key encryption to encrypt the message."""

    # Convert the public key into PEM format for use in RSA encryption.
    pem_key = f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"
    rsa_public_key = RSA.importKey(pem_key)
    rsa_public_key = PKCS1_OAEP.new(rsa_public_key, hashAlgo=SHA256)

    # Encrypt the message
    message = str.encode(message)
    encrypted_text = rsa_public_key.encrypt(message)
    encrypted_text_b64 = b64encode(encrypted_text)
    return encrypted_text_b64
