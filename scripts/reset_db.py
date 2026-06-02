"""
Reset the SQLite database.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database.models import Base
from src.database.db import engine


def reset_database():

    Base.metadata.drop_all(bind=engine)

    print("Old tables deleted")

    Base.metadata.create_all(bind=engine)

    print("New tables created")


if __name__ == "__main__":
    reset_database()