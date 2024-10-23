import requests
import json
import os
from dotenv import load_dotenv
import time
from rich.console import Console
from spot import get_bateman_video
from imgur.imgur import upload_video_imgur
from spot import get_spotify_track_data
from datetime import datetime

load_dotenv()
console = Console()


def get_creds() -> dict:
    """This function is used to get the credentials from the environment variables. It returns a dictionary containing the credentials.

    Returns:
        dict: dictionary containing access token, client id, client secret, graph domain, graph version, endpoint base, page id, instagram account id, and instagram username
    """

    creds = dict()
    creds["access_token"] = os.environ.get("FB_ACCESS_TOKEN")
    creds["client_id"] = os.environ.get("FB_CLIENT_ID")
    creds["client_secret"] = os.environ.get("FB_CLIENT_SECRET")
    creds["graph_domain"] = os.environ.get("GRAPH_DOMAIN")
    creds["graph_version"] = os.environ.get("GRAPH_VERSION")
    creds["endpoint_base"] = creds["graph_domain"] + creds["graph_version"] + "/"
    creds["page_id"] = os.environ.get("PAGE_ID")
    creds["instagram_account_id"] = os.environ.get("INSTAGRAM_ACCOUNT_ID")
    creds["ig_username"] = os.environ.get("IG_USERNAME")
    console.print("Loaded Environment Variables for Instagram API")
    return creds


def facebook_api_call(url: str, endpointParams: dict, type: str) -> dict:
    """Request data from endpoint with params. This function is used to make calls to the Facebook API. It returns the response from the API.

    Args:
        url (str): string of the url endpoint to make request from
        endpoint_params (dict): dictionary keyed by the names of the url parameters
        type (str): type of request to be made. Can be "GET" or "POST"


    Returns:
        dict: dictionary containing the response from the API, the url, and the endpoint params used to make the request

    """

    if type == "POST":
        data = requests.post(url, endpointParams)
    else:
        data = requests.get(url, endpointParams)

    response = dict()
    response["url"] = url
    response["endpoint_params"] = endpointParams
    response["json_data"] = json.loads(data.content)

    # console.print("Response from Facebook API is as follows:")
    # console.print("URL:")
    # console.print(response["url"])
    # console.print("Endpoint Params:")
    # console.print(response["endpoint_params"])
    # console.print("Response:")
    # console.print(response["json_data"])

    return response


def create_media_object(params: dict) -> dict:
    """Create something called media object. this is step 1 of the process of publishing content to instagram. This function is used to create a media object on Instagram. It returns the response from the API.

    Args:
            params (dict): dictionary of params

    API Endpoint:
            https://graph.facebook.com/v21.0/{ig-user-id}/media?image_url={image-url}&caption={caption}&access_token={access-token}
            https://graph.facebook.com/v21.0/{ig-user-id}/media?video_url={video-url}&caption={caption}&access_token={access-token}

    Returns:
            dict: dictionary containing the response from the API, the url, and the endpoint params used to make the request

    """

    url = params["endpoint_base"] + params["instagram_account_id"] + "/media"

    endpoint_params = dict()
    endpoint_params["caption"] = params["caption"]
    endpoint_params["access_token"] = params["access_token"]

    if "IMAGE" == params["media_type"]:
        endpoint_params["image_url"] = params["media_url"]
        console.print(
            f"Creating media object for image [b #FF69B4]{params['media_url']}[/b #FF69B4] on Instagram"
        )
    else:
        endpoint_params["media_type"] = params["media_type"]
        endpoint_params["video_url"] = params["media_url"]
        console.print(
            f"Creating media object for video [b #FF69B4]{params['media_url']}[/b #FF69B4] on Instagram"
        )
    return facebook_api_call(url, endpoint_params, "POST")


def get_media_object_status(media_object_id: int, params: dict) -> dict:
    """Check the status of a media object.

    Args:
        media_object_id (int): id of the media object
        params (dict): dictionary of params

    API Endpoint:
        https://graph.facebook.com/v21.0/{ig-container-id}?fields=status_code

    Returns:
        dict: dictionary containing the response from the API, the url, and the endpoint params used to make the request

    """

    url = params["endpoint_base"] + "/" + media_object_id

    endpoint_params = dict()
    endpoint_params["fields"] = "status_code"
    endpoint_params["access_token"] = params["access_token"]

    return facebook_api_call(url, endpoint_params, "GET")


def publish_media(media_object_id: int, params: dict) -> dict:
    """Publish content to Instagram.

    Args:
            media_object_id (int): id of the media object
            params (dict): dictionary of params

    API Endpoint:
            https://graph.facebook.com/v21.0/{ig-user-id}/media_publish?creation_id={creation-id}&access_token={access-token}

    Returns:
            dict: dictionary containing the response from the API, the url, and the endpoint params used to make the request

    """

    url = params["endpoint_base"] + params["instagram_account_id"] + "/media_publish"

    endpoint_params = dict()
    endpoint_params["creation_id"] = media_object_id
    endpoint_params["access_token"] = params["access_token"]

    return facebook_api_call(url, endpoint_params, "POST")


def publish_image(params: dict, image_url: str, caption: str):
    """Publish image to Instagram.

    Args:
        params (dict): parameters to be passed
        image_url (str): url of the image
        caption (str): Instagram caption
    """
    params["media_type"] = "IMAGE"
    params["media_url"] = image_url
    params["caption"] = caption

    image_media_object_response = create_media_object(params)

    image_media_object_id = image_media_object_response["json_data"]["id"]
    image_media_status_code = "IN_PROGRESS"

    console.print(
        f"Image Media Object ID [b #DC143C]{image_media_object_id}[/b #DC143C] : Creating media object on Instagram"
    )
    console.print("[i #FFB6C1]This can take more than a minute[/i #FFB6C1]")

    with console.status("Publishing image", spinner="dots") as status:
        while image_media_status_code != "FINISHED":
            image_media_object_status_response = get_media_object_status(
                image_media_object_id, params
            )
            image_media_status_code = image_media_object_status_response["json_data"][
                "status_code"
            ]
            if image_media_status_code == "ERROR":
                console.print(
                    f"[b red]Error while publishing video:[/b red] [b #DC143C]{image_media_object_status_response}[/b #DC143C]"
                )
            time.sleep(5)

    console.print(
        f"Image Media Object ID [b #DC143C]{image_media_object_id}[/b #DC143C] : Publishing on Instagram"
    )
    publish_image_response = publish_media(image_media_object_id, params)

    console.print(
        f"Published Video ID: [b #DC143C]{publish_image_response['json_data']['id']}[/b #DC143C] : Published image successfully"
    )


def publish_video(params: dict, video_url: str, caption: str):
    """Publish video to Instagram.

    Args:
        params (dict): parameters to be passed
        video_url (str): url of the video
        caption (str): Instagram caption
    """
    params["media_type"] = "REELS"
    params["media_url"] = video_url
    params["caption"] = caption

    video_media_object_response = create_media_object(params)

    video_media_object_id = video_media_object_response["json_data"]["id"]
    video_media_status_code = "IN_PROGRESS"

    console.print(
        f"Video Media Object ID [b #DC143C]{video_media_object_id}[/b #DC143C] : Creating media object on Instagram"
    )
    console.print("[i #FFB6C1]This can take more than a minute[/i #FFB6C1]")

    with console.status("Publishing video", spinner="dots") as status:
        while video_media_status_code != "FINISHED":
            video_media_object_status_response = get_media_object_status(
                video_media_object_id, params
            )
            video_media_status_code = video_media_object_status_response["json_data"][
                "status_code"
            ]
            if video_media_status_code == "ERROR":
                console.print(
                    f"[b red]Error while publishing video:[/b red] [b #DC143C]{video_media_object_status_response}[/b #DC143C]"
                )
            time.sleep(5)

    console.print(
        f"Video Media Object ID [b #DC143C]{video_media_object_id}[/b #DC143C] : Publishing on Instagram"
    )
    publish_video_response = publish_media(video_media_object_id, params)

    console.print(
        f"Published Video ID: [b #DC143C]{publish_video_response['json_data']['id']}[/b #DC143C] : Published video successfully"
    )


def get_content_publishing_limit(params: dict) -> dict:
    """Get the api limit for the user

    Args:
        params: dictionary of params

    API Endpoint:
        https://graph.facebook.com/v21.0/{ig-user-id}/content_publishing_limit?fields=config,quota_usage

    Returns:
        dict: dictionary containing the response from the API, the url, and the endpoint params used to make the request

    """

    url = (
        params["endpoint_base"]
        + params["instagram_account_id"]
        + "/content_publishing_limit"
    )

    endpoint_params = dict()
    endpoint_params["fields"] = "config,quota_usage"
    endpoint_params["access_token"] = params["access_token"]
    return facebook_api_call(url, endpoint_params, "GET")


def main(spotify_track_url: str):
    if (video_path := get_bateman_video(spotify_track_url)) is None:
        print("Bateman Video could not be generated")
        return

    video_link = upload_video_imgur(
        video_path,
        "Patrick Bateman",
        "I have to return some video tapes",
    )

    params = get_creds()
    # Generating Caption
    track = get_spotify_track_data(spotify_track_url)
    artist_names = [track["artists"][i]["name"] for i in range(len(track["artists"]))]
    track_name = track["name"]

    start_date = datetime(2024, 10, 23) # Inception
    today = datetime.now()
    days_difference = (today - start_date).days

    ig_caption = f"Day {days_difference} of returning videotapes\n🎶 {', '.join(artist_names)} - {track_name} \n#PatrickBateman"
    console.print("Caption:")
    console.print(ig_caption)
    publish_video(params, video_link, ig_caption)

    limit = get_content_publishing_limit(params)

    quota_total = limit['json_data']['data'][0]['config']['quota_total']
    quota_dutation = limit['json_data']['data'][0]['config']['quota_duration']
    quota_usage = limit['json_data']['data'][0]['quota_usage']
    console.print("Content Publishing API Limit:")
    console.print(f"Total Quota: {quota_total}")
    console.print(f"Quota Duration: {quota_dutation}")
    console.print(f"Quota Usage: {quota_usage}")


if __name__ == "__main__":
    main("https://open.spotify.com/track/5Y6nVaayzitvsD5F7nr3DV?si=99c5eae0c17f4df1")
