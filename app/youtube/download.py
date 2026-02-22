"""
This module can download from both Youtube and Youtube Music. It downloads both audio and thumnbails.
"""

from pathlib import Path
import yt_dlp
from app.config import console
from typing import TypedDict
from PIL import Image

from app.youtube.image import crop_square_from_horizontal_middle
from app.youtube.utils import HeatmapPoint


class SongData(TypedDict):
    audio_path: Path | str
    heatmap: list[HeatmapPoint] | None
    thumbnail_path: Path
    video_id: str
    title: str
    channel: str
    source_url: str
    duration_seconds: int | None


def _print_song_metadata(info: dict) -> None:
    video_id = info.get("id", "unknown")
    title = info.get("title", "unknown")
    channel = info.get("uploader") or info.get("channel") or "unknown"
    source_url = info.get("webpage_url") or "unknown"
    duration = info.get("duration")

    console.print(
        f"[bold #FFC0CB]video-id      :[/bold #FFC0CB] [#DDA0DD]{video_id}[/#DDA0DD]"
    )
    console.print(
        f"[bold #FFC0CB]title         :[/bold #FFC0CB] [#DDA0DD]{title}[/#DDA0DD]"
    )
    console.print(
        f"[bold #FFC0CB]channel       :[/bold #FFC0CB] [#DDA0DD]{channel}[/#DDA0DD]"
    )
    console.print(
        f"[bold #FFC0CB]source-url    :[/bold #FFC0CB] [#DDA0DD]{source_url}[/#DDA0DD]"
    )
    console.print(
        f"[bold #FFC0CB]duration-sec  :[/bold #FFC0CB] [#DDA0DD]{duration}[/#DDA0DD]"
    )


def _find_moved_thumbnail_path(info: dict, thumbnail_dir: Path) -> Path:
    video_id = info.get("id")
    if not video_id:
        raise RuntimeError(
            "yt-dlp info did not contain a video id for thumbnail lookup"
        )

    candidates = sorted(thumbnail_dir.glob(f"{video_id}.*"))
    if not candidates:
        raise RuntimeError(
            f"Could not find moved thumbnail in {thumbnail_dir} for video id {video_id}"
        )

    picked = candidates[-1]
    console.print(
        f"Video [bold]{video_id}[/bold] -> Using downloaded thumbnail [bold]{picked}[/bold]"
    )
    return picked


def _get_downloaded_thumbnail_path(info: dict, thumbnail_dir: Path) -> Path:
    thumbnails = info.get("thumbnails") or []
    video_id = info.get("id", "unknown")
    console.print(
        f"Video [bold]{video_id}[/bold] -> Thumbnail sources in metadata: [bold]{len(thumbnails)}[/bold]"
    )
    final_path = _find_moved_thumbnail_path(info, thumbnail_dir)
    if not final_path.is_file():
        raise RuntimeError(f"Resolved thumbnail path does not exist: {final_path}")

    with Image.open(final_path) as image:
        console.print(
            f"Video [bold]{video_id}[/bold] -> Thumbnail before crop: [bold]{image.size[0]}x{image.size[1]}[/bold]"
        )
        cropped = crop_square_from_horizontal_middle(image)
        cropped.save(final_path)
        console.print(
            f"Video [bold]{video_id}[/bold] -> Thumbnail after crop: [bold]{cropped.size[0]}x{cropped.size[1]}[/bold]"
        )
    return final_path


def download_song_youtube(url: str) -> SongData:
    """downloads video using yt_dlp and extracts audio from it. Also downloads thumbnail.

    Args:
        url (str): url to song on youtube

    Returns:
        str: path of the downloaded song
    """

    output_location = {}

    def hook(d):
        if d["status"] == "finished":
            output_location["filename"] = d["filename"]
            console.print(
                f"Downloaded audio successfully to [bold]{d['filename']}[/bold]"
            )

    audio_dir = Path("./assets/audio/youtube")
    thumbnail_dir = Path("./assets/thumbnails/youtube")
    audio_dir.mkdir(exist_ok=True, parents=True)
    thumbnail_dir.mkdir(exist_ok=True, parents=True)
    thumbnail_dir_abs = thumbnail_dir.resolve()
    console.print(f"Audio directory      : [bold]{audio_dir.resolve()}[/bold]")
    console.print(f"Thumbnail directory  : [bold]{thumbnail_dir_abs}[/bold]")

    ydl_opts = {
        "format": "m4a/bestaudio/best",
        "writethumbnail": True,
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "aac",
            }
        ],
        "paths": {
            "home": str(audio_dir),
            "thumbnail": str(thumbnail_dir_abs),
        },
        "outtmpl": {
            "default": "%(title)s.%(ext)s",
            "thumbnail": "%(id)s.%(ext)s",
        },
        "progress_hooks": [hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        console.print("Downloading audio and thumbnail from YouTube")
        info = ydl.extract_info(url, download=True)
        sanitized_info = ydl.sanitize_info(info)
        _print_song_metadata(sanitized_info)
        heatmap = sanitized_info.get("heatmap")
        if heatmap is None:
            console.print("yt-dlp metadata does not include heatmap data")
        else:
            console.print(f"yt-dlp returned [bold]{len(heatmap)}[/bold] heatmap points")
        thumbnail_path = _get_downloaded_thumbnail_path(sanitized_info, thumbnail_dir)
    console.print("YouTube audio+thumbnail download pipeline completed")
    return {
        "audio_path": output_location.get(
            "filename", "Download failed or file not found"
        ),
        "heatmap": heatmap,
        "thumbnail_path": thumbnail_path,
        "video_id": sanitized_info.get("id", ""),
        "title": sanitized_info.get("title", ""),
        "channel": sanitized_info.get("uploader")
        or sanitized_info.get("channel")
        or "",
        "source_url": sanitized_info.get("webpage_url", ""),
        "duration_seconds": sanitized_info.get("duration"),
    }


def download_thumbnail_youtube(url: str) -> Path:
    """Download only thumbnail(s) for a YouTube URL using yt_dlp."""

    thumbnail_dir = Path("./assets/thumbnails/youtube")
    thumbnail_dir.mkdir(exist_ok=True, parents=True)
    console.print(f"Thumbnail directory  : [bold]{thumbnail_dir.resolve()}[/bold]")

    ydl_opts = {
        "skip_download": True,
        "writethumbnail": True,
        "paths": {"thumbnail": str(thumbnail_dir)},
        "outtmpl": {"thumbnail": "%(id)s.%(ext)s"},
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        console.print(f"Downloading thumbnail only for [bold]{url}[/bold]")
        info = ydl.extract_info(url, download=True)
        sanitized_info = ydl.sanitize_info(info)
        _print_song_metadata(sanitized_info)
        thumbnail_path = _get_downloaded_thumbnail_path(sanitized_info, thumbnail_dir)
        console.print(
            f"Downloaded thumbnail successfully to [bold]{thumbnail_path}[/bold]"
        )
        return thumbnail_path


if __name__ == "__main__":
    download_song_youtube(
        "https://music.youtube.com/watch?v=bQD-mcJUbR4&si=GRSw5BdZC4nmXsDV"
    )
