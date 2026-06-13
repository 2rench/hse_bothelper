import requests


def download_file(url: str) -> bytes:

    headers = {
        "User-Agent":
        "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=60,
    )

    response.raise_for_status()

    return response.content
