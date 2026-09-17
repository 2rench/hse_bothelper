import os

from fastapi import (
    FastAPI,
    HTTPException,
)
from fastapi.responses import (
    Response,
    RedirectResponse,
)

from app.database.user_repository import (
    get_user_by_calendar_token,
)

from app.services.calendar_service import (
    build_calendar,
)


app = FastAPI(
    title="HSE Schedule Calendar",
)


@app.get(
    "/",
)
async def root():

    return {
        "status": "ok",
    }


@app.get(
    "/calendar/{token}.ics",
)
async def calendar(
    token: str,
):

    user = get_user_by_calendar_token(
        token
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="Calendar not found",
        )

    content = build_calendar(
        user["group_name"],
        user["excluded_subjects"],
    )

    return Response(
        content=content,
        media_type="text/calendar",
        headers={
            "Content-Disposition": (
                'inline; filename="hse.ics"'
            ),
            "Cache-Control": "no-cache",
        },
    )


@app.get(
    "/calendar/{token}/subscribe",
)
async def calendar_subscribe(
    token: str,
):
    """
    Редирект на webcal:// — браузер/система
    откроет приложение календаря с окном подписки.
    """

    user = get_user_by_calendar_token(
        token
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="Calendar not found",
        )

    base_url = os.getenv(
        "CALENDAR_BASE_URL",
        "",
    ).rstrip("/")

    if not base_url:

        raise HTTPException(
            status_code=500,
            detail="CALENDAR_BASE_URL is not set",
        )

    host = (
        base_url
        .replace("https://", "")
        .replace("http://", "")
    )

    webcal_url = (
        f"webcal://{host}"
        f"/calendar/{token}.ics"
    )

    return RedirectResponse(
        url=webcal_url,
        status_code=302,
    )
