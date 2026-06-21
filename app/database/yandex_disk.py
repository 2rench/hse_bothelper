import os
import yadisk

disk = yadisk.YaDisk(
    token=os.getenv(
        "YANDEX_DISK_TOKEN"
    )
)


def upload_file(
    local_path,
    remote_path,
):

    if not disk.exists(
        "/backups"
    ):

        disk.mkdir(
            "/backups"
        )

    if disk.exists(
        remote_path
    ):

        disk.remove(
            remote_path
        )

    disk.upload(
        local_path,
        remote_path
    )


def list_backups():

    return list(
        disk.listdir(
            "/backups"
        )
    )


def delete_file(
    path,
):

    if disk.exists(
        path
    ):

        disk.remove(
            path
        )
