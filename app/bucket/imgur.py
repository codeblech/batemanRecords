"""
The purpose of this module is to take in a video_path, upload it to Imgur, and return its URL.
"""

import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()


def upload_video_imgur(video_path, title, description):
    client_id = os.getenv("IMGUR_CLIENT_ID")
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
