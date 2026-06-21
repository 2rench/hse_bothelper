from pathlib import Path
from datetime import datetime
import subprocess

from app.config import DATABASE_URL


def create_backup():

    Path(
        "files/backups"
    ).mkdir(
        parents=True,
        exist_ok=True,
    )

    now = datetime.now().strftime(
        "%Y-%m-%d_%H-%M"
    )

    filename = (
        f"files/backups/"
        f"backup_{now}.dump"
    )

    subprocess.run(
        [
            "pg_dump",
            "-Fc",
            DATABASE_URL,
            "-f",
            filename,
        ],
        check=True,
    )

    return filename
