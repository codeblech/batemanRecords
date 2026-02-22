"""
This module has the old way of downloading thumbnails. It still works, but now I prefer downloading both the audio
and the thumbnail using yt-dlp. We use the Youtube Thumbnail downloader in this module
as fallback when yt-dlp doesn't work.
"""

from pathlib import Path
import requests
from PIL import Image
from io import BytesIO
import re
from bs4 import BeautifulSoup

from app.config import console
from app.youtube.image import crop_square_from_horizontal_middle


# this function is taken from https://gist.github.com/rodrigoborgesdeoliveira/987683cfbfcc8d800192da1e73adc486?permalink_comment_id=5097394#gistcomment-5097394
def get_youtube_video_id_by_url(url) -> str:
    regex = r"^((https?://(?:www\.)?(?:m\.)?youtube\.com))/((?:oembed\?url=https?%3A//(?:www\.)youtube.com/watch\?(?:v%3D)(?P<video_id_1>[\w\-]{10,20})&format=json)|(?:attribution_link\?a=.*watch(?:%3Fv%3D|%3Fv%3D)(?P<video_id_2>[\w\-]{10,20}))(?:%26feature.*))|(https?:)?(\/\/)?((www\.|m\.)?youtube(-nocookie)?\.com\/((watch)?\?(app=desktop&)?(feature=\w*&)?v=|embed\/|v\/|e\/)|youtu\.be\/)(?P<video_id_3>[\w\-]{10,20})"
    match = re.match(regex, url, re.IGNORECASE)
    if match:
        return (
            match.group("video_id_1")
            or match.group("video_id_2")
            or match.group("video_id_3")
        )
    else:
        raise RuntimeError(
            f"The video_id could not be extraced from the youtube video url -> {url}"
        )


def get_yt_thumbnail(url: str) -> Path:
    """Get the thumbnail of a song using its youtube music url

    Args:
        url (str): YouTube url to the song

    Returns:
        str | None: path to the downloaded thumbail image file
    """
    console.print(f"Attempting YouTube thumbnail fallback for [bold]{url}[/bold]")
    try:
        video_id = get_youtube_video_id_by_url(url)
    except RuntimeError:
        console.print(
            "Could not parse a standard YouTube video id. Falling back to YouTube Music thumbnail parsing"
        )
        return get_ytmusic_thumbnail(url)
    save_dir = Path("./assets/thumbnails/youtube")
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / f"{video_id}.jpg"

    # check if this thumbnail is already available, and return it if it exists
    if save_path.is_file():
        console.print(
            f"Video [bold]{video_id}[/bold] -> Using already downloaded fallback thumbnail [bold]{save_path}[/bold]"
        )
        return save_path

    thumbnail_url: str = "https://img.youtube.com/vi/" + video_id + "/maxresdefault.jpg"
    console.print(f"Video [bold]{video_id}[/bold] -> Downloading thumbnail from {thumbnail_url}")

    response = requests.get(thumbnail_url)
    response.raise_for_status()
    with Image.open(BytesIO(response.content)) as im:
        console.print(
            f"Video [bold]{video_id}[/bold] -> Downloaded fallback thumbnail size: [bold]{im.size[0]}x{im.size[1]}[/bold]"
        )
        cropped = crop_square_from_horizontal_middle(im).convert("RGB")
        console.print(
            f"Video [bold]{video_id}[/bold] -> Cropped fallback thumbnail size: [bold]{cropped.size[0]}x{cropped.size[1]}[/bold]"
        )
        cropped.save(save_path, format="JPEG")
        console.print(
            f"Saved fallback thumbnail to [bold]{save_path}[/bold]"
        )
        return save_path


def get_ytmusic_thumbnail(url: str) -> Path:
    """Get the thumbnail of a song, playlist, or album using its youtube music url

    Args:
        link (str): YouTube Music url to the song

    Returns:
        str | None: path to the downloaded thumbail image file
    """
    console.print(f"Attempting YouTube Music thumbnail fallback for [bold]{url}[/bold]")
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.content, "lxml")
    # print(f"soup: {soup.prettify()}")
    title_tags = soup.find_all("title")  # ytmusic returns two title tags in html

    thumbnail_url = None
    if title_tags and "Your browser is deprecated" in str(title_tags[0]):
        meta = soup.find("meta", {"property": "og:image"})
        if meta is not None:
            thumbnail_url = meta.get("content", None)
            console.print(
                f"Found YouTube Music fallback thumbnail URL: [bold]{thumbnail_url}[/bold]"
            )

    if thumbnail_url is not None:
        rr = requests.get(thumbnail_url)
        rr.raise_for_status()
        save_name = re.findall(r".*=(.*)", url)[0]  # extract last part of url
        save_dir = Path("./assets/thumbnails/youtube")
        save_dir.mkdir(exist_ok=True, parents=True)
        save_path = save_dir / f"{save_name}.jpg"
        with Image.open(BytesIO(rr.content)) as im:
            console.print(
                f"YTMusic fallback thumbnail size: [bold]{im.size[0]}x{im.size[1]}[/bold]"
            )
            cropped = crop_square_from_horizontal_middle(im).convert("RGB")
            console.print(
                f"YTMusic cropped thumbnail size: [bold]{cropped.size[0]}x{cropped.size[1]}[/bold]"
            )
            cropped.save(save_path, format="JPEG")
            console.print(
                f"Saved YTMusic fallback thumbnail to [bold]{save_path}[/bold]"
            )
            return save_path
    else:
        console.print("[bold red]Could not find thumbnail metadata on YouTube Music page[/bold red]")
        raise RuntimeError("Could not download YTMusic Thumbnail")


if __name__ == "__main__":
    get_yt_thumbnail(
        "https://music.youtube.com/watch?v=COz9lDCFHjw&si=_9sdj_2Cf53mELk4"
    )
