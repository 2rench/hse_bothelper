from app.database.yandex_disk import (
    list_backups,
    delete_file,
)


def cleanup_backups():

    files = sorted(
        list_backups(),
        key=lambda x: x.modified
    )

    if len(files) <= 3:
        return

    old_files = files[:-3]

    for file in old_files:

        print(
            "DELETE OLD BACKUP:",
            file.path
        )

        delete_file(
            file.path
        )
