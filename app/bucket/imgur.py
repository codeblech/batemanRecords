"""
Imgur bucket provider (primary).

Uploads a local video file to Imgur and returns the public media URL.
This is the first provider attempted by `app.bucket.main.upload_to_bucket`.
"""

import requests
import os
import json

from app.config import config


def upload_video_imgur(video_path, title, description):
    """Upload a video to Imgur and return the resulting public link."""
    client_id = config.imgur_client_id()
    url = "https://api.imgur.com/3/image"

    payload = {"type": "file", "title": title, "description": description}
    files = [
        ("video", (os.path.basename(video_path), open(video_path, "rb"), "video/mp4"))
    ]
    headers = {"Authorization": f"Client-ID {client_id}"}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.content)
    return json.loads(response.content)["data"]["link"]


if __name__ == "__main__":
    try:
        video_link = upload_video_imgur(
            "./outputs/combined/combined_02-36-31.mp4",
            "Simple upload",
            "This is a simple image upload in Imgur",
        )
        print(f"\nImgur upload successful! Video link: {video_link}")
    except Exception as e:
        print(f"\nError during Imgur upload: {str(e)}")
