import requests


TIMETABLE_URL = (
    "https://disk.360.yandex.ru/d/At7POE_VL0oNiA"
)

YANDEX_API_URL = (
    "https://cloud-api.yandex.net/v1/disk/public/resources"
)

YANDEX_DOWNLOAD_URL = (
    "https://cloud-api.yandex.net/v1/disk/public/resources/download"
)


def get_schedule_files():

    response = requests.get(
        YANDEX_API_URL,
        params={
            "public_key": TIMETABLE_URL,
            "limit": 1000,
        },
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()

    files = []

    embedded = data.get(
        "_embedded",
        {},
    )

    items = embedded.get(
        "items",
        [],
    )

    for item in items:

        if item.get("type") != "file":
            continue

        name = item.get(
            "name",
            "",
        )

        name_lower = name.lower()

        if not (
            name_lower.endswith(".xls")
            or
            name_lower.endswith(".xlsx")
        ):
            continue

        path = item.get(
            "path"
        )

        if not path:
            continue

        download_response = requests.get(
            YANDEX_DOWNLOAD_URL,
            params={
                "public_key": TIMETABLE_URL,
                "path": path,
            },
            timeout=30,
        )

        download_response.raise_for_status()

        download_data = (
            download_response.json()
        )

        download_url = download_data.get(
            "href"
        )

        if not download_url:
            continue

        files.append(
            {
                "name": name,
                "url": download_url,
            }
        )

    return files
