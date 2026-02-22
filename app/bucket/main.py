from app.bucket.imgur import upload_video_imgur
from app.bucket.tmpfiles import upload_video_tmpfiles


def upload_to_bucket(video_path, title, description):
    try:
        return upload_video_imgur(video_path, title, description)
    except Exception as imgur_error:
        print(f"Imgur upload failed, falling back to tmpfiles.org: {imgur_error}")
        return upload_video_tmpfiles(video_path=video_path)
