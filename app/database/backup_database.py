import os
import subprocess
from datetime import datetime

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)


def create_backup():

    now = datetime.now().strftime(
        "%Y-%m-%d_%H-%M"
    )

    filename = (
        f"files/backups/"
        f"backup_{now}.sql"
    )

    subprocess.run(
        [
            "pg_dump",
            DATABASE_URL,
            "-f",
            filename,
        ]
    )

    return filename
