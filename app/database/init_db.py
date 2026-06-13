from app.database.database import Base
from app.database.database import engine
from app.database.user_model import User

from app.database.models import Lesson
from app.database.schedule_file_model import (
    ScheduleFile,
)
from app.database.schedule_version_model import (
    ScheduleVersion,
)

def init_db():

    Base.metadata.create_all(bind=engine)

    print("Database initialized")

if __name__ == '__main__':

    init_db()
