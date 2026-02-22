from app.application import get_creds, facebook_api_call
import datetime
from rich.console import Console


def debug_facebook_access_token(params: dict) -> dict:
    """
    Get info about the access token set in .env as FB_ACCESS_TOKEN.
    API Endpoint: https://graph.facebook.com/debug_token?input_token={input-token}&access_token={valid-access-token}

    Args:
        params (dict): params from .env

    Returns:
        dict: response from the endpoint. Contains the data_access_expires_at and expires_at
    """
    endpointParams = dict()
    endpointParams["input_token"] = params["access_token"]
    endpointParams["access_token"] = params["access_token"]

    url = params["graph_domain"] + "debug_token"

    return facebook_api_call(url, endpointParams, "GET")


if __name__ == "__main__":
    params = get_creds()
    response = debug_facebook_access_token(params)
    console = Console()
    console.print("\nData Access Expires at: ")
    console.print(
        datetime.datetime.fromtimestamp(
            response["json_data"]["data"]["data_access_expires_at"]
        )
    )

    console.print("\nToken Expires at: ")
    console.print(
        datetime.datetime.fromtimestamp(response["json_data"]["data"]["expires_at"])
    )
