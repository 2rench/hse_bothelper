from pathlib import Path

from app.database.backup_database import (
    create_backup,
)

from app.database.yandex_disk import (
    upload_file,
)


def backup_and_upload():

    local_file = (
        create_backup()
    )

    file_name = Path(
        local_file
    ).name

    upload_file(
        local_file,
        f"/backups/{file_name}"
    )

    Path(
        local_file
    ).unlink(
        missing_ok=True
    )

    print(
        "BACKUP UPLOADED:",
        file_name
    )
