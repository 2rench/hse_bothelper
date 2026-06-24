from datetime import datetime

from app.database.group_repository import (
    clear_groups,
)


def refresh_groups_if_needed():

    now = datetime.now()

    month = now.month
    day = now.day

    if month == 1 and day == 1:

        clear_groups()

    elif month == 9 and day in [1, 5]:

        clear_groups()
