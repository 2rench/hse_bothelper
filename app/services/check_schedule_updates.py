import re

from pathlib import Path

from sqlalchemy.orm import Session

from app.database.database import (
    SessionLocal,
)

from app.database.schedule_file_model import (
    ScheduleFile,
)

from app.services.hse_schedule_scraper import (
    get_schedule_files,
)

from app.services.file_downloader import (
    download_file,
)

from app.services.file_hash import (
    calculate_hash,
)

from app.services.file_storage import (
    save_file,
)

from app.services.schedule_importer import (
    import_schedule,
)

from app.services.schedule_cleanup import (
    delete_schedule,
)


def check_updates():

    updates = []
    files = get_schedule_files()

    for item in files:
        db: Session = SessionLocal()
        name = item["name"].lower()

        if (
            "неделя" not in name
            and
            "сессия" not in name
        ):
            db.close()
            continue
        content = download_file(
            item["url"]
        )

        current_hash = calculate_hash(
            content
        )

        existing = (
            db.query(ScheduleFile)
            .filter(
                ScheduleFile.file_url
                == item["url"]
            )
            .first()
        )

        # Новый файл
        if existing is None:

            print(
                "NEW FILE:",
                item["name"]
            )

            saved_path = save_file(
                item["name"],
                content,
            )

            db.commit()
            db.close()

            import_schedule(
                str(saved_path)
            )

            Path(saved_path).unlink(
                missing_ok=True
            )

            db = SessionLocal()

            db.add(
                ScheduleFile(
                    file_name=item["name"],
                    file_url=item["url"],
                    file_hash=current_hash,
                )
            )
            db.commit()
            db.close()

            updates.append(
                {
                    "type": "new",
                    "name": item["name"],
                    "week": extract_week_number(
                        item["name"]
                    ),
                    "is_session": (
                        "сессия"
                        in item["name"].lower()
                    ),
                }
            )
            continue

        if (
            existing.file_hash
            != current_hash
        ):

            print(
                "UPDATED:",
                item["name"]
            )

            saved_path = save_file(
                item["name"],
                content,
            )

            try:

                deleted = delete_schedule(
                    db,
                    item["name"],
                )

                db.commit()

                print(
                    f"DELETED LESSONS: {deleted}"
                )

                success = import_schedule(
                    str(saved_path)
                )

                if not success:

                    db.rollback()
                    db.close()
                    continue

                Path(saved_path).unlink(
                    missing_ok=True
                )

                existing.file_hash = (
                    current_hash
                )

                db.commit()

                print(
                    "REIMPORTED:",
                    item["name"]
                )
                updates.append(
                    {
                        "type": "new",
                        "name": item["name"],
                        "week": extract_week_number(
                            item["name"]
                        ),
                        "is_session": (
                            "сессия"
                            in item["name"].lower()
                        ),
                    }
                )

            except Exception as e:

                db.rollback()

                print(
                    "IMPORT ERROR:",
                    e,
                )
            finally:
                db.close()

    return updates


def extract_week_number(
    name: str,
) -> int:

    match = re.search(
        r"неделя №(\d+)",
        name,
    )

    if not match:
        return 0

    return int(
        match.group(1)
    )

if __name__ == "__main__":

    check_updates()
