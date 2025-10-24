
from dotenv import load_dotenv
import os
import json
import requests


load_dotenv()
OPENFIGI_API_KEY = os.getenv("OPEN_FIGI_API_KEY")
OPENFIGI_BASE_URL = "https://api.openfigi.com"


JsonType = None | int | str | bool | list["JsonType"] | dict[str, "JsonType"]


def api_call(path: str, data: dict | None = None, method: str = "POST") -> JsonType:
    """
    Make an api call to `api.openfigi.com`.
    
    Args:
        path (str): API endpoint, for example "/v3/search, /v3/mapping, /v3/filter"
        method (str, optional): HTTP request method. Defaults to "POST".
        data (dict | None, optional): HTTP request data. Defaults to None.

    Returns:
        JsonType: Response of the api call parsed as a JSON object
    """

    url = OPENFIGI_BASE_URL + path

    headers = {"Content-Type": "application/json"}
    if OPENFIGI_API_KEY:
        headers["X-OPENFIGI-APIKEY"] = OPENFIGI_API_KEY

    
    response = requests.request(
        method=method,
        url=url,
        json=data,
        headers=headers,
    )
    
    response.raise_for_status()  # Exception if HTTP error
    return response.json()

