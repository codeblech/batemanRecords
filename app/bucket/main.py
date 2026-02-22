"""
Bucket upload orchestrator.

Why this layer exists:
- The Instagram Graph API publish step requires a public, retrievable media URL.
- The generated video is local, so it must be uploaded to a temporary/public host first.

Provider order:
1. Imgur (primary)
2. tmpfiles.org (fallback)
"""

from app.bucket.imgur import upload_video_imgur
from app.bucket.tmpfiles import upload_video_tmpfiles


def upload_to_bucket(video_path, title, description):
    """Upload video to a public host and return a direct URL usable by Instagram."""
    try:
        return upload_video_imgur(video_path, title, description)
    except Exception as imgur_error:
        print(f"Imgur upload failed, falling back to tmpfiles.org: {imgur_error}")
        return upload_video_tmpfiles(video_path=video_path)
