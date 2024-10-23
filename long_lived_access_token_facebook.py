from app import get_creds, facebook_api_call
from rich.console import Console


def get_long_lived_access_token(params: dict) -> dict:
    """
    Get long lived access token from a short lived access token. client_id, client_secret, and access_token are required in the params.
    API Endpoint: https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}

    Args:
        params (dict): params from .env file. Required keys are client_id, client_secret, access_token, endpoint_base

    Returns:
        dict: response from the endpoint. Contains the long lived access token.

    """

    endpoint_params = dict()
    endpoint_params["grant_type"] = "fb_exchange_token"
    endpoint_params["client_id"] = params["client_id"]
    endpoint_params["client_secret"] = params["client_secret"]
    endpoint_params["fb_exchange_token"] = params["access_token"]

    url = params["endpoint_base"] + "oauth/access_token"

    return facebook_api_call(url, endpoint_params, "GET")


if __name__ == "__main__":
    params = get_creds()

    response = get_long_lived_access_token(params)

    console = Console()
    console.print("Access Token:")
    console.print(response["json_data"]["access_token"])
