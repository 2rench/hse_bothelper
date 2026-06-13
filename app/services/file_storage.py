from pathlib import Path


DOWNLOAD_DIR = Path(
    "files/downloaded"
)

DOWNLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def save_file(
    filename: str,
    content: bytes,
) -> Path:
    """
    Сохраняет файл на диск.
    """

    safe_name = (
        filename
        .replace("/", "_")
        .replace("\\", "_")
    )

    file_path = (
        DOWNLOAD_DIR
        / f"{safe_name}.xls"
    )

    with open(
        file_path,
        "wb",
    ) as file:

        file.write(content)

    return file_path
