import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database.models import Base
from src.database.db import engine


def create_database():

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "Database created successfully"
    )


if __name__ == "__main__":
    create_database()