"""
Utility for refreshing Imgur OAuth tokens.

This module is intentionally side-effect free on import so it can be documented
by Sphinx autodoc without performing network calls.
"""

import requests

from app.config import config


def generate_imgur_access_token() -> str:
    """Request a refreshed Imgur token payload and return response text."""
    url = "https://api.imgur.com/oauth2/token"

    payload = {
        "refresh_token": config.imgur_refresh_token(),
        "client_id": config.imgur_client_id(),
        "client_secret": config.imgur_client_secret(),
        "grant_type": "refresh_token",
    }

    response = requests.post(url, data=payload)
    return response.text


if __name__ == "__main__":
    print(generate_imgur_access_token())
