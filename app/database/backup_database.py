import os
import subprocess
from datetime import datetime


def create_backup():

    database_url = os.getenv(
        "DATABASE_URL"
    )

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
            database_url,
            "-f",
            filename,
        ]
    )

    return filename
