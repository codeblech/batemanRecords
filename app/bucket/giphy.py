"""
The purpose of this module is to take in a video_path, upload it to Giphy, and return its URL.
Giphy only allows uploading videos with audio in its Clips API. But, that API is approval-only.
This module is useless now.
"""

import json
import mimetypes
import os

import requests
from dotenv import load_dotenv

load_dotenv()


def upload_video_giphy(
    video_path=None,
    tags=None,
    source_post_url=None,
    username=None,
    country_code=None,
    region=None,
    source_image_url=None,
):
    api_key = os.getenv("GIPHY_API_KEY")
    if not api_key:
        raise ValueError("Missing GIPHY_API_KEY in environment.")

    if not video_path and not source_image_url:
        raise ValueError("Provide either video_path or source_image_url.")

    url = "https://upload.giphy.com/v1/gifs"
    payload = {"api_key": api_key}

    if username:
        payload["username"] = username
    if tags:
        payload["tags"] = tags
    if source_post_url:
        payload["source_post_url"] = source_post_url
    if country_code:
        payload["country_code"] = country_code
    if region:
        payload["region"] = region
    if source_image_url:
        payload["source_image_url"] = source_image_url

    files = None
    file_handle = None
    if video_path:
        mime_type = mimetypes.guess_type(video_path)[0] or "application/octet-stream"
        file_handle = open(video_path, "rb")
        files = {"file": (os.path.basename(video_path), file_handle, mime_type)}

    try:
        response = requests.post(url, data=payload, files=files)
    finally:
        if file_handle:
            file_handle.close()

    print(response.content)
    response_json = json.loads(response.content)
    if "data" in response_json and "id" in response_json["data"]:
        giphy_id = response_json["data"]["id"]
        return f"https://media.giphy.com/media/{giphy_id}/giphy.mp4"
    else:
        raise RuntimeError(f"GIPHY upload failed with response: {response_json}")


if __name__ == "__main__":
    try:
        giphy_id = upload_video_giphy(
            video_path="./outputs/combined/combined_02-36-31.mp4",
            tags="bateman,edit",
        )
        print(f"\nGIPHY upload successful! GIF ID: {giphy_id}")
    except Exception as e:
        print(f"\nError during GIPHY upload: {str(e)}")
