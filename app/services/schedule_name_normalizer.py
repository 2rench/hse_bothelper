import re


def normalize_schedule_name(
    name: str,
) -> str:

    return re.sub(
        r"\s+с изм\..*$",
        "",
        name,
        flags=re.IGNORECASE,
    ).strip()
