import re
import hashlib
import json

from collections import defaultdict
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


def find_existing_file(
    db: Session,
    schedule_key: str,
):
    files = (
        db.query(ScheduleFile)
        .all()
    )

    for file in files:

        if extract_schedule_key(
            file.file_name
        ) == schedule_key:

            return file

    return None


def get_group_signatures(
    schedule_key: str,
) -> dict[str, str]:

    db: Session = SessionLocal()

    try:

        lessons = (
            db.query(Lesson)
            .filter(
                Lesson.schedule_key == schedule_key
            )
            .all()
        )

    finally:

        db.close()

    grouped = defaultdict(list)

    for lesson in lessons:

        grouped[
            lesson.group_name
        ].append(
            (
                lesson.day or "",
                lesson.date or "",
                lesson.lesson_number or "",
                lesson.lesson_time or "",
                lesson.subject or "",
                lesson.lesson_type or "",
                lesson.teacher or "",
                lesson.room or "",
                lesson.building or "",
                bool(lesson.is_online),
            )
        )

    signatures = {}

    for group_name, group_lessons in grouped.items():

        group_lessons.sort()

        payload = json.dumps(
            group_lessons,
            ensure_ascii=False,
            separators=(
                ",",
                ":",
            ),
        )

        signatures[group_name] = (
            hashlib.sha256(
                payload.encode("utf-8")
            ).hexdigest()
        )

    return signatures


def check_updates():

    updates = []

    files = get_schedule_files()

    actual_keys = set()

    for item in files:

        schedule_key = (
            extract_schedule_key(
                item["name"]
            )
        )

        actual_keys.add(
            schedule_key
        )

        name = item["name"].lower()

        if "сессия" in name:

            schedule_type = "session"

        elif "неделя" in name:

            schedule_type = "changes"

        elif "базовое" in name:

            schedule_type = "base"

        else:

            continue

        db: Session = SessionLocal()

        existing = find_existing_file(
            db,
            schedule_key,
        )

        content = download_file(
            item["url"]
        )

        current_hash = calculate_hash(
            content
        )

        if existing is None:

            print(
                "NEW FILE:",
                item["name"]
            )

            saved_path = save_file(
                item["name"],
                content,
            )

            success = import_schedule(
                str(saved_path),
                schedule_type,
                schedule_key,
            )

            Path(
                saved_path
            ).unlink(
                missing_ok=True
            )

            if success:

                groups = sorted(
                    get_group_signatures(
                        schedule_key
                    ).keys()
                )

                db.add(
                    ScheduleFile(
                        file_name=item["name"],
                        file_url=item["url"],
                        file_hash=current_hash,
                    )
                )

                db.commit()

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
                        "groups": groups,
                    }
                )

            db.close()

            continue

        if existing.file_hash == current_hash:

            db.close()

            continue

        print(
            "UPDATED:",
            item["name"]
        )

        old_group_signatures = (
            get_group_signatures(
                schedule_key
            )
        )

        saved_path = save_file(
            item["name"],
            content,
        )

        try:

            success = import_schedule(
                str(saved_path),
                schedule_type,
                schedule_key,
            )

            if success:

                new_group_signatures = (
                    get_group_signatures(
                        schedule_key
                    )
                )

                all_groups = (
                    set(
                        old_group_signatures
                    )
                    |
                    set(
                        new_group_signatures
                    )
                )

                changed_groups = sorted(
                    group
                    for group in all_groups
                    if (
                        old_group_signatures.get(
                            group
                        )
                        !=
                        new_group_signatures.get(
                            group
                        )
                    )
                )

                existing.file_name = (
                    item["name"]
                )

                existing.file_url = (
                    item["url"]
                )

                existing.file_hash = (
                    current_hash
                )

                db.commit()

                Path(
                    saved_path
                ).unlink(
                    missing_ok=True
                )

                print(
                    "REIMPORTED:",
                    item["name"]
                )

                if changed_groups:

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
                            "groups": changed_groups,
                        }
                    )

        except Exception as error:

            db.rollback()

            print(
                "IMPORT ERROR:",
                error,
            )

        finally:

            Path(
                saved_path
            ).unlink(
                missing_ok=True
            )

            db.close()

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

            db.query(
                Lesson
            ).filter(
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
