from app import get_creds, facebook_api_call
from rich.console import Console


def get_user_pages(params: dict) -> dict:
    """
    Get facebook pages for a user. access_token is required in the params.
    API Endpoint: https://graph.facebook.com/{graph-api-version}/me/accounts?access_token={access-token}

    Args:
            params (dict): params from .env file. Required keys are access_token, endpoint_base

    Returns:
            object: data from the endpoint. It contains the page id, name, and category
    """

    endpointParams = dict()
    endpointParams["access_token"] = params["access_token"]

    url = params["endpoint_base"] + "me/accounts"

    return facebook_api_call(url, endpointParams, "GET")


if __name__ == "__main__":
    params = get_creds()
    response = get_user_pages(params)

    console = Console()
    console.print("\n---- FACEBOOK PAGE INFO ----\n")
    console.print("Page Name:")
    console.print(response["json_data"]["data"][0]["name"])
    console.print("\nPage Category:")
    console.print(response["json_data"]["data"][0]["category"])
    console.print("\nPage Id:")
    console.print(response["json_data"]["data"][0]["id"])
