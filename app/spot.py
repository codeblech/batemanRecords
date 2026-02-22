"""
This module's purpose is to expose a function `get_bateman_video()` that takes in a spotify track URL, generates the upload-able
bateman video, and returns the file path to that video.
"""

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import requests
from tqdm import tqdm
import subprocess
from rich.console import Console

load_dotenv()

console = Console()


def download_thumbnail_spotify(thumbnail_url: str, track_id: str) -> str | None:
    """
    Download cover art of a track using its URL. This URL the thumbnail URL, not the track URL. Also shows a progress bar.

    Args:
        thumbnail_url (str): URL of the cover art
        track_id (str): track_id of the track. Required to save the image with the track_id as the name

    Returns:
        str | None: Returns the path to the downloaded image.
        If the image is already downloaded, it returns the path to the already downloaded image.
        If the image is not available, it returns None.
    """
    save_name = track_id
    save_path = os.path.join("./assets/thumbnails/spotify", f"{save_name}.jpg")
    os.makedirs("./assets/thumbnails/spotify", exist_ok=True)

    # check if this thumbnail is already available, and return it if it exists
    try:
        with open(save_path) as im:
            console.print(
                f"Track [bold]{track_id}[/bold] -> Using already downloaded spotify thumbnail"
            )
        return save_path
    except:
        pass

    try:
        console.print(f"Track [bold]{track_id}[/bold] -> Downloading thumbnail")
        response = requests.get(thumbnail_url, stream=True)
        if response.status_code != 200:
            return None

        # Get total file size from headers
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024  # 1 KB

        # Create progress bar
        progress_bar = tqdm(
            total=total_size,
            unit="iB",
            unit_scale=True,
            desc=f"Downloading Thumbnail",
            colour="white",
            ncols=80,  # Set width of progress bar
            leave=True,  # Keep the progress bar after completion
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        )

        # Write the content to file with progress updates
        with open(save_path, "wb") as f:
            for data in response.iter_content(block_size):
                f.write(data)
                progress_bar.update(len(data))

        progress_bar.close()
        console.print(f"Downloaded thumbnail successfully to [bold]{save_path}[/bold]")
        return save_path
    except Exception as e:
        console.print(f"[bold red]Error downloading thumbnail:[/bold red] {e}")
        return None


def download_spotify_preview(track_preview_url: str, track_id: str) -> str | None:
    """
    Downloads 30second preview of a track using its URL. Also shows a progress bar.

    Args:
        track_preview_url (str): URL of the preview track. This is different from the track URL
        track_id (str): used to save the audio file with the track_id as the name

    Returns:
        str | None: returns the path to the downloaded audio file. If the audio is already downloaded, it returns the path to the already downloaded audio file. If the audio is not available, it returns None.
    """
    save_path = os.path.join("./assets/audio/spotify", f"{track_id}.mp3")
    os.makedirs("./assets/audio/spotify", exist_ok=True)

    if os.path.exists(save_path):
        console.print(
            f"Track [bold]{track_id}[/bold] -> Using already downloaded audio file"
        )
        return save_path

    response = requests.get(track_preview_url, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024

        with (
            open(save_path, "wb") as f,
            tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                desc=f"Downloading Audio",
                colour="white",
                ncols=80,  # Set width of progress bar
                leave=True,  # Keep the progress bar after completion
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
            ) as pbar,
        ):
            for data in response.iter_content(block_size):
                f.write(data)
                pbar.update(len(data))
        console.print(f"Downloaded audio successfully to [bold]{save_path}[/bold]")
        return save_path
    else:
        console.print(
            f"[bold red]Failed to download audio. Status code:[/bold red] {response.status_code}"
        )
        return None


def generate_video(bg_image_path: str) -> str:
    """
    Generate patrick bateman walking to music video using the given background image. Also shows a progress bar.

    Args:
        bg_image_path (str): path to the background image  (cover art)

    Returns:
        str: path to the output video
    """
    with console.status("Generating Video", spinner="dots"):
        result = subprocess.run(
            ["scripts/generateVideoSpotify.sh", bg_image_path], capture_output=True
        )
        # print("generate stdout: ", result.stdout)
        # print("generate stderr: ", result.stderr)
        output_video_path = str(result.stdout).lstrip("b'").rstrip("\\n'")
    console.print(f"output video path (only video): [bold]{output_video_path}[/bold]")
    return output_video_path


def combine_audio_video(video_path: str, audio_path: str) -> str:
    """
    Combines the given audio and video with delay added from start of the audio.

    Args:
        video_path (str): path to the video
        audio_path (str): path to the audio

    Returns:
        str: final output video path
    """
    result = subprocess.run(
        [
            "scripts/combineAudioVideo.sh",
            audio_path,
            video_path,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    # print("combine stdout: ", result.stdout)
    # print("combine stderr: ", result.stderr)
    final_video_path = result.stdout.strip()
    console.print(f"final output path (with audio): [b]{final_video_path}[/b]")
    return final_video_path


def get_spotify_track_data(url: str) -> dict:
    """
    Get the track data from the spotify URL

    Args:
        url (str): spotify URL of the track

    Returns:
        dict: track data
    """
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
    track = sp.track(url)
    return track


def get_bateman_video(url: str) -> str | None:
    """
    Generates a video of Patrick Bateman walking to the music of the given spotify track URL. The video is generated by combining the cover art of the track and the 30-second preview of the track. The video is generated using the generateVideoSpotify.sh script and the audio is combined with the video using the combineAudioVideo.sh script. The final video is saved in the assets folder.

    Args:
        url (str): spotify URL of the song

    Returns:
        str | None: path to the final output video. If the track does not have a preview URL, it returns None.
    """
    track = get_spotify_track_data(url)
    track_id = track["id"]
    artist_names = [track["artists"][i]["name"] for i in range(len(track["artists"]))]
    track_name = track["name"]
    if track.get("preview_url") is None:
        console.print("[bold red]This track does not have a preview URL[/bold red]")
        console.print(
            f"[bold #FFC0CB]track-id      : [/bold #FFC0CB][#DDA0DD]{track_id}[/#DDA0DD]"
        )
        console.print(
            f"[bold #FFC0CB]artists       : [/bold #FFC0CB][#DDA0DD]{artist_names}[/#DDA0DD]"
        )
        console.print(
            f"[bold #FFC0CB]track-name    : [/bold #FFC0CB][#DDA0DD]{track_name}[/#DDA0DD]"
        )
        return None
    track_preview_url = track["preview_url"]
    track_thumbnail_url = track["album"]["images"][0]["url"]
    console.print(
        f"[bold #FFC0CB]track-id      :[/bold #FFC0CB] [#DDA0DD]{track_id}[/#DDA0DD]"
    )
    console.print(
        f"[bold #FFC0CB]track-name    :[/bold #FFC0CB] [#DDA0DD]{track_name}[/#DDA0DD]"
    )
    console.print(
        f"[bold #FFC0CB]artists       :[/bold #FFC0CB] [#DDA0DD]{artist_names}[/#DDA0DD]"
    )
    console.print(
        f"[bold #FFC0CB]audio         :[/bold #FFC0CB] [#DDA0DD]{track_preview_url}[/#DDA0DD]"
    )
    console.print(
        f"[bold #FFC0CB]cover art     :[/bold #FFC0CB] [#DDA0DD]{track_thumbnail_url}[/#DDA0DD]"
    )

    bg_image_path = download_thumbnail_spotify(track_thumbnail_url, track_id)
    audio_path = download_spotify_preview(track_preview_url, track_id)
    video_path = generate_video(bg_image_path)
    final_video_path = combine_audio_video(video_path, audio_path)
    return final_video_path


if __name__ == "__main__":
    get_bateman_video(
        "https://open.spotify.com/track/5Y6nVaayzitvsD5F7nr3DV?si=99c5eae0c17f4df1"
    )
