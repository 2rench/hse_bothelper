import hashlib
import hmac
import json
import os
import random
import time

from datetime import datetime, timedelta
from pathlib import Path
from typing import Literal
from urllib.parse import parse_qsl

from fastapi import (
    FastAPI,
    HTTPException,
    Request,
)
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()

from app.database.database import SessionLocal

from app.database.user_model import User

from app.database.user_repository import (
    get_user,
    get_user_group,
    set_theme,
    toggle_schedule_updates,
    toggle_tomorrow_notifications,
    get_or_create_calendar_token,
)

from app.services.schedule_service import (
    get_lessons_by_date,
    get_week_lessons_by_number,
    get_available_week_numbers,
    get_current_schedule_week,
)

from app.database.session_repository import (
    get_all_sessions,
    get_session_lessons,
)

from app.bot.services.formatter import (
    THEMES,
)


BASE_DIR = Path(__file__).resolve().parent

STATIC_DIR = BASE_DIR / "static"

BOT_TOKEN = os.getenv("BOT_TOKEN")

CALENDAR_BASE_URL = os.getenv(
    "CALENDAR_BASE_URL"
)


app = FastAPI(
    title="HSE Mini App",
)


app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


THEME_NAMES = {
    "default": "Классика",
    "luxury": "Люкс",
    "clean_girl": "Мягкий",
    "brother": "Контраст",
    "it_style": "Техно",
    "english": "Английский",
    "french": "Французский",
    "chinese": "Китайский",
}


THEME_SYMBOLS = {
    "default": "○",
    "luxury": "✦",
    "clean_girl": "♡",
    "brother": "⚡",
    "it_style": ">_",
    "english": "A",
    "french": "É",
    "chinese": "文",
}


GIRL_THEMES = {
    "luxury",
    "clean_girl",
}

BOY_THEMES = {
    "brother",
    "it_style",
}

LANGUAGE_THEMES = {
    "english": "en",
    "french": "fr",
    "chinese": "zh",
}


GREETINGS_GIRL_RU = [
    "Выглядишь супер",
    "Ты сегодня особенно хороша",
    "Сияешь ярче солнца",
    "Красотка, день будет отличным",
    "Улыбнись — тебе идёт",
    "Неотразима, как всегда",
    "Прекрасна в каждой детали",
    "Умница и красавица",
]

GREETINGS_BOY_RU = {
    "morning": "Доброе утро",
    "day": "Добрый день",
    "evening": "Добрый вечер",
    "night": "Доброй ночи",
}

GREETINGS_EN = {
    "morning": "Good morning",
    "day": "Good afternoon",
    "evening": "Good evening",
    "night": "Good night",
}

GREETINGS_FR = {
    "morning": "Bonjour",
    "day": "Bon après-midi",
    "evening": "Bonsoir",
    "night": "Bonne nuit",
}

GREETINGS_ZH = {
    "morning": "早上好",
    "day": "下午好",
    "evening": "晚上好",
    "night": "晚安",
}


def _time_of_day() -> str:

    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "morning"
    if 12 <= hour < 17:
        return "day"
    if 17 <= hour < 23:
        return "evening"
    return "night"


def build_greeting(
    theme_id: str,
    telegram_id: int,
) -> str:

    part_of_day = _time_of_day()

    if theme_id in LANGUAGE_THEMES:

        lang = LANGUAGE_THEMES[theme_id]

        if lang == "en":
            return GREETINGS_EN[part_of_day]
        if lang == "fr":
            return GREETINGS_FR[part_of_day]
        if lang == "zh":
            return GREETINGS_ZH[part_of_day]

    if theme_id in GIRL_THEMES:

        return random.choice(
            GREETINGS_GIRL_RU
        )

    return GREETINGS_BOY_RU[
        part_of_day
    ]


class ThemeRequest(BaseModel):
    theme: str


class ExcludedSubjectRequest(BaseModel):
    subject: str


class NotificationToggleRequest(BaseModel):
    field: Literal[
        "schedule_updates",
        "tomorrow_notifications",
    ]


def validate_init_data(
    init_data: str,
) -> dict:

    if not BOT_TOKEN:
        raise HTTPException(
            status_code=500,
            detail="BOT_TOKEN is not configured",
        )

    parsed = dict(
        parse_qsl(
            init_data,
            keep_blank_values=True,
        )
    )

    received_hash = parsed.pop(
        "hash",
        None,
    )

    if not received_hash:
        raise HTTPException(
            status_code=401,
            detail="Invalid Telegram data",
        )

    data_check_string = "\n".join(
        f"{key}={value}"
        for key, value in sorted(
            parsed.items()
        )
    )

    secret_key = hmac.new(
        key=b"WebAppData",
        msg=BOT_TOKEN.encode(),
        digestmod=hashlib.sha256,
    ).digest()

    calculated_hash = hmac.new(
        key=secret_key,
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(
        calculated_hash,
        received_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Telegram signature",
        )

    auth_date = parsed.get(
        "auth_date"
    )

    if auth_date:
        try:
            auth_timestamp = int(
                auth_date
            )
        except ValueError:
            raise HTTPException(
                status_code=401,
                detail="Invalid auth_date",
            )

        max_age = int(
            os.getenv(
                "MINIAPP_INIT_DATA_MAX_AGE",
                "86400",
            )
        )

        if (
            abs(
                int(time.time())
                - auth_timestamp
            )
            > max_age
        ):
            raise HTTPException(
                status_code=401,
                detail="Telegram data expired",
            )

    user_data = parsed.get(
        "user"
    )

    if not user_data:
        raise HTTPException(
            status_code=401,
            detail="Telegram user not found",
        )

    try:
        user = json.loads(
            user_data
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Telegram user",
        )

    return user


def get_identity(
    request: Request,
) -> dict:

    init_data = request.headers.get(
        "X-Telegram-Init-Data"
    )

    if not init_data:

        dev_id = os.getenv(
            "MINIAPP_DEV_TELEGRAM_ID"
        )

        if dev_id:

            return {
                "id": int(dev_id),
                "first_name": "Developer",
            }

        raise HTTPException(
            status_code=401,
            detail="Telegram initData is missing",
        )

    return validate_init_data(
        init_data
    )


def get_telegram_id(
    request: Request,
) -> int:

    return int(
        get_identity(request)["id"]
    )


def serialize_lesson(
    lesson,
) -> dict:

    return {
        "id": lesson.id,
        "day": lesson.day,
        "date": lesson.date,
        "lesson_number": lesson.lesson_number,
        "lesson_time": lesson.lesson_time,
        "subject": lesson.subject,
        "lesson_type": lesson.lesson_type,
        "teacher": lesson.teacher,
        "room": lesson.room,
        "building": lesson.building,
        "is_online": lesson.is_online,
    }


def get_user_payload(
    telegram_id: int,
) -> dict:

    user = get_user(
        telegram_id
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    excluded_subjects = (
        user.get(
            "excluded_subjects",
            [],
        )
        or []
    )

    return {
        "telegram_id": telegram_id,
        "group_name": user.get(
            "group_name"
        ),
        "schedule_updates": bool(
            user.get(
                "schedule_updates",
                True,
            )
        ),
        "tomorrow_notifications": bool(
            user.get(
                "tomorrow_notifications",
                False,
            )
        ),
        "theme": user.get(
            "theme",
            "default",
        ),
        "excluded_subjects": excluded_subjects,
    }


def serialize_theme(
    theme_id: str,
) -> dict:

    theme = THEMES.get(
        theme_id
    )

    if theme is None:
        theme = THEMES["default"]

    return {
        "id": theme_id,
        "name": THEME_NAMES.get(
            theme_id,
            theme_id,
        ),
        "symbol": THEME_SYMBOLS.get(
            theme_id,
            "○",
        ),
        "tokens": {
            "no_lessons": theme.get(
                "no_lessons",
                "Пар нет",
            ),
            "pairs": theme.get(
                "pairs",
                "Пар",
            ),
            "day": theme.get(
                "day",
                "📅",
            ),
            "lesson": theme.get(
                "lesson",
                "◦",
            ),
            "subject": theme.get(
                "subject",
                "•",
            ),
            "type": theme.get(
                "type",
                "•",
            ),
            "room": theme.get(
                "room",
                "•",
            ),
            "online": theme.get(
                "online",
                "Онлайн",
            ),
        },
    }


@app.get("/")
async def index():

    return FileResponse(
        STATIC_DIR / "index.html"
    )


@app.get("/health")
async def health():

    return {
        "status": "ok"
    }


@app.get("/api/bootstrap")
async def bootstrap(
    request: Request,
):

    telegram_id = get_telegram_id(
        request
    )

    identity = get_identity(
        request
    )

    user = get_user_payload(
        telegram_id
    )

    current_theme = (
        user["theme"]
    )

    themes = [
        serialize_theme(
            theme_id
        )
        for theme_id in THEMES
    ]

    return {
        "identity": {
            "id": telegram_id,
            "first_name": identity.get(
                "first_name",
                "",
            ),
            "username": identity.get(
                "username",
                "",
            ),
        },
        "user": user,
        "theme": serialize_theme(
            current_theme
        ),
        "themes": themes,
    }


@app.get("/api/weeks")
async def weeks(
    request: Request,
):

    telegram_id = get_telegram_id(
        request
    )

    group = get_user_group(
        telegram_id
    )

    if not group:

        return {
            "weeks": [],
            "current_week": None,
            "default_week": None,
        }

    weeks = get_available_week_numbers(
        group
    )

    current_week = get_current_schedule_week(
        group
    )

    default_week = (
        current_week
        if current_week in weeks
        else (weeks[0] if weeks else None)
    )

    return {
        "weeks": weeks,
        "current_week": current_week,
        "default_week": default_week,
    }


@app.get("/api/schedule")
async def schedule(
    request: Request,
    view: Literal[
        "today",
        "tomorrow",
        "week",
    ] = "today",
    week: int | None = None,
):

    telegram_id = get_telegram_id(
        request
    )

    user = get_user_payload(
        telegram_id
    )

    group = user[
        "group_name"
    ]

    if not group:

        return {
            "view": view,
            "lessons": [],
            "empty_message": "Сначала выбери группу.",
        }

    excluded = set(
        user[
            "excluded_subjects"
        ]
    )

    if view == "today":

        date = datetime.now().strftime(
            "%d.%m.%Y"
        )

        lessons = (
            get_lessons_by_date(
                group,
                date,
            )
        )

        empty_message = (
            "На сегодня пар нет."
        )

    elif view == "tomorrow":

        date = (
            datetime.now()
            + timedelta(days=1)
        ).strftime(
            "%d.%m.%Y"
        )

        lessons = (
            get_lessons_by_date(
                group,
                date,
            )
        )

        empty_message = (
            "На завтра пар нет."
        )

    else:

        current_week = get_current_schedule_week(
            group
        )

        target_week = (
            week
            if week is not None
            else current_week
        )

        lessons = []

        if target_week is not None:

            lessons = (
                get_week_lessons_by_number(
                    group,
                    target_week,
                )
            )

        week = target_week

        empty_message = (
            "На этой неделе пар нет."
        )

    lessons = [
        lesson
        for lesson in lessons
        if lesson.subject
        not in excluded
    ]

    greeting = None

    if view == "today":

        greeting = build_greeting(
            user.get(
                "theme",
                "default",
            ),
            telegram_id,
        )

    return {
        "view": view,
        "group": group,
        "week": week if view == "week" else None,
        "greeting": greeting,
        "lessons": [
            serialize_lesson(
                lesson
            )
            for lesson in lessons
        ],
        "empty_message": empty_message,
    }


@app.get("/api/sessions")
async def sessions(
    request: Request,
):

    telegram_id = get_telegram_id(
        request
    )

    group = get_user_group(
        telegram_id
    )

    if not group:

        return {
            "sessions": []
        }

    return {
        "sessions": get_all_sessions()
    }


@app.get(
    "/api/sessions/{session_name:path}"
)
async def session_schedule(
    session_name: str,
    request: Request,
):

    telegram_id = get_telegram_id(
        request
    )

    group = get_user_group(
        telegram_id
    )

    if not group:

        raise HTTPException(
            status_code=400,
            detail="Group is not selected",
        )

    lessons = get_session_lessons(
        group,
        session_name,
    )

    return {
        "session": session_name,
        "lessons": [
            serialize_lesson(
                lesson
            )
            for lesson in lessons
        ],
    }


@app.get(
    "/api/excluded-subjects"
)
async def excluded_subjects(
    request: Request,
):

    telegram_id = get_telegram_id(
        request
    )

    group = get_user_group(
        telegram_id
    )

    if not group:

        return {
            "subjects": [],
            "excluded": [],
        }

    user = get_user_payload(
        telegram_id
    )

    current_week = get_current_schedule_week(
        group
    )

    lessons = []

    if current_week is not None:

        lessons = (
            get_week_lessons_by_number(
                group,
                current_week,
            )
        )

    subjects = sorted(
        {
            lesson.subject
            for lesson in lessons
            if lesson.subject
        },
        key=lambda value: value.casefold(),
    )

    return {
        "subjects": subjects,
        "excluded": user[
            "excluded_subjects"
        ],
    }


@app.post(
    "/api/excluded-subjects/toggle"
)
async def toggle_excluded_subject(
    payload: ExcludedSubjectRequest,
    request: Request,
):

    telegram_id = get_telegram_id(
        request
    )

    group = get_user_group(
        telegram_id
    )

    if not group:

        raise HTTPException(
            status_code=400,
            detail="Group is not selected",
        )

    subject = payload.subject.strip()

    if not subject:

        raise HTTPException(
            status_code=400,
            detail="Subject is empty",
        )

    db = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(
                User.telegram_id
                == telegram_id
            )
            .first()
        )

        if not user:

            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        excluded = list(
            user.excluded_subjects
            or []
        )

        if subject in excluded:

            excluded.remove(
                subject
            )

        else:

            excluded.append(
                subject
            )

        user.excluded_subjects = (
            excluded
        )

        db.commit()

        return {
            "excluded": excluded
        }

    finally:

        db.close()


@app.post("/api/theme")
async def update_theme(
    payload: ThemeRequest,
    request: Request,
):

    telegram_id = get_telegram_id(
        request
    )

    if payload.theme not in THEMES:

        raise HTTPException(
            status_code=400,
            detail="Unknown theme",
        )

    set_theme(
        telegram_id,
        payload.theme,
    )

    return {
        "theme": serialize_theme(
            payload.theme
        )
    }


@app.post(
    "/api/notifications/toggle"
)
async def notification_toggle(
    payload: NotificationToggleRequest,
    request: Request,
):

    telegram_id = get_telegram_id(
        request
    )

    if payload.field == "schedule_updates":

        toggle_schedule_updates(
            telegram_id
        )

    else:

        toggle_tomorrow_notifications(
            telegram_id
        )

    user = get_user_payload(
        telegram_id
    )

    return {
        "schedule_updates": user[
            "schedule_updates"
        ],
        "tomorrow_notifications": user[
            "tomorrow_notifications"
        ],
    }


@app.get("/api/calendar")
async def calendar(
    request: Request,
):

    telegram_id = get_telegram_id(
        request
    )

    token = get_or_create_calendar_token(
        telegram_id
    )

    if token is None:

        raise HTTPException(
            status_code=404,
            detail="Calendar token not found",
        )

    if not CALENDAR_BASE_URL:

        raise HTTPException(
            status_code=500,
            detail="CALENDAR_BASE_URL is not configured",
        )

    base_url = CALENDAR_BASE_URL.rstrip(
        "/"
    )

    https_url = (
        f"{base_url}"
        f"/calendar/{token}.ics"
    )

    webcal_url = https_url.replace(
        "https://",
        "webcal://",
        1,
    )

    return {
        "https_url": https_url,
        "webcal_url": webcal_url,
    }
