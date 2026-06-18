import re

from pathlib import Path
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.database.models import Lesson
from app.database.schedule_file_model import ScheduleFile

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


def extract_schedule_key(
    name: str,
) -> str:

    name = name.lower()

    match = re.search(
        r"неделя №(\d+)",
        name,
    )

    if match:

        week = match.group(1)

        if "сессия" in name:
            return f"session_{week}"

        if "базовое" in name:
            return "base"

        return f"changes_{week}"

    return name


def check_updates():

    updates = []

    files = get_schedule_files()

    actual_keys = set()

    for item in files:

        actual_keys.add(
            extract_schedule_key(
                item["name"]
            )
        )

        db: Session = SessionLocal()

        name = item["name"].lower()

        if "сессия" in name:

            schedule_type = "session"

        elif "неделя" in name:

            schedule_type = "changes"

        elif "базовое" in name:

            schedule_type = "base"

        else:

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

            schedule_key = extract_schedule_key(
                item["name"]
            )

            import_schedule(
                str(saved_path),
                schedule_type,
                schedule_key,
            )

            Path(saved_path).unlink(
                missing_ok=True
            )

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
                        in name
                    ),
                }
            )

            continue

        # Изменённый файл
        if existing.file_hash != current_hash:

            print(
                "UPDATED:",
                item["name"]
            )

            saved_path = save_file(
                item["name"],
                content,
            )

            try:

                schedule_key = extract_schedule_key(
                    item["name"]
                )

                success = import_schedule(
                    str(saved_path),
                    schedule_type,
                    schedule_key,
                )

                if success:

                    existing.file_hash = current_hash

                    db.commit()

                    Path(saved_path).unlink(
                        missing_ok=True
                    )

                    print(
                        "REIMPORTED:",
                        item["name"]
                    )

                    updates.append(
                        {
                            "type": "updated",
                            "name": item["name"],
                            "week": extract_week_number(
                                item["name"]
                            ),
                            "is_session": (
                                "сессия"
                                in name
                            ),
                        }
                    )

            except Exception as error:

                db.rollback()

                print(
                    "IMPORT ERROR:",
                    error,
                )

            finally:

                db.close()

        else:

            db.close()

    # Удаляем расписания,
    # которых больше нет на сайте

    db = SessionLocal()

    db_keys = (
        db.query(
            Lesson.schedule_key
        )
        .distinct()
        .all()
    )

    for row in db_keys:

        key = row[0]

        if key is None:
            continue

        if key not in actual_keys:

            print(
                f"DELETE OLD {key}"
            )

            db.query(Lesson).filter(
                Lesson.schedule_key == key
            ).delete()

    db.commit()
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
