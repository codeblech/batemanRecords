from app import get_creds, facebook_api_call
from rich.console import Console


def get_instagram_account(params: dict) -> dict:
    """
    Get instagram_account_id. page_id should be known and present in the params.
    API Endpoint: https://graph.facebook.com/{graph-api-version}/{page-id}?access_token={your-access-token}&fields=instagram_business_account

    Args:
        params (dict): params from .env file. Required keys are page_id, access_token, endpoint_base

    Returns:
        dict: data from the endpoint. It contains instagram_business_account id

    """

    endpointParams = dict()
    endpointParams["access_token"] = params["access_token"]
    endpointParams["fields"] = "instagram_business_account"

    url = params["endpoint_base"] + params["page_id"]

    return facebook_api_call(url, endpointParams, "GET")


if __name__ == "__main__":
    params = get_creds()
    response = get_instagram_account(params)
    console = Console()
    console.print("\n---- INSTAGRAM ACCOUNT INFO ----\n")
    console.print("Page Id:")
    console.print(response["json_data"]["id"])
    console.print("\nInstagram Business Account Id:")
    console.print(response["json_data"]["instagram_business_account"]["id"])
