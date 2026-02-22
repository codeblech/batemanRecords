"""
Upload a local file to tmpfiles.org and return the uploaded file URL.
"""

import json
import os

import requests
from app.config import console


def upload_video_tmpfiles(video_path):
    url = "https://tmpfiles.org/api/v1/upload"

    with open(video_path, "rb") as file_handle:
        files = {
            "file": (
                os.path.basename(video_path),
                file_handle,
                "application/octet-stream",
            )
        }
        response = requests.post(url, files=files)

    console.print(f"Response from tmpfiles API: \n{response.content}")
    response_json = json.loads(response.content)
    dashboard_url = response_json["data"]["url"]
    console.print(f"Dashboard URL -> {dashboard_url}")
    download_url = dashboard_url.replace(
        "http://tmpfiles.org/", "http://tmpfiles.org/dl/"
    )
    console.print(f"Download URL -> {download_url}")
    return download_url


if __name__ == "__main__":
    try:
        video_link = upload_video_tmpfiles("./outputs/combined/combined_02-36-31.mp4")
        print(f"\ntmpfiles upload successful! File link: {video_link}")
    except Exception as e:
        print(f"\nError during tmpfiles upload: {str(e)}")
