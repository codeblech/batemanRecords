import os
from typing import Any

from dotenv import load_dotenv
from rich.console import Console

console = Console()


class Config:
    def __init__(self) -> None:
        # Load .env once and centralize env access for the app.
        load_dotenv()

    @staticmethod
    def get(name: str, default: Any = None) -> str | Any:
        return os.getenv(name, default)

    @staticmethod
    def require(name: str) -> str:
        value = os.getenv(name)
        if not value:
            raise ValueError(f"Missing required environment variable: {name}")
        return value

    def instagram_creds(self) -> dict[str, str]:
        graph_domain = self.require("GRAPH_DOMAIN")
        graph_version = self.require("GRAPH_VERSION")
        return {
            "access_token": self.require("FB_ACCESS_TOKEN"),
            "client_id": self.require("FB_CLIENT_ID"),
            "client_secret": self.require("FB_CLIENT_SECRET"),
            "graph_domain": graph_domain,
            "graph_version": graph_version,
            "endpoint_base": f"{graph_domain}{graph_version}/",
            "page_id": self.require("PAGE_ID"),
            "instagram_account_id": self.require("INSTAGRAM_ACCOUNT_ID"),
            "ig_username": self.require("IG_USERNAME"),
        }

    def giphy_api_key(self) -> str | None:
        return self.get("GIPHY_API_KEY")

    def imgur_client_id(self) -> str:
        return self.require("IMGUR_CLIENT_ID")

    def imgur_refresh_token(self) -> str:
        return self.require("IMGUR_REFRESH_TOKEN")

    def imgur_client_secret(self) -> str:
        return self.require("IMGUR_CLIENT_SECRET")


config = Config()
