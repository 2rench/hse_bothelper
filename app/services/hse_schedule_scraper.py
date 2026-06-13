import requests

from bs4 import BeautifulSoup

from urllib.parse import urljoin


TIMETABLE_URL = (
    "https://perm.hse.ru/students/timetable/"
)


def get_schedule_files():

    response = requests.get(
        TIMETABLE_URL,
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    files = []

    for link in soup.find_all("a"):

        href = link.get("href")

        if not href:
            continue

        href_lower = href.lower()

        if not (
            href_lower.endswith(".xls")
            or
            href_lower.endswith(".xlsx")
        ):
            continue

        name = link.get_text(
            strip=True
        )

        href = urljoin(
            TIMETABLE_URL,
            href,
        )

        files.append(
            {
                "name": name,
                "url": href,
            }
        )

    return files
