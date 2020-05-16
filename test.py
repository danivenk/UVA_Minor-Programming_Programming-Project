from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from app.models import db, User

# Configure database
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# set up database
engine = create_engine(os.getenv("DATABASE_URL"))
ssess = scoped_session(sessionmaker(bind=engine))
db.metadata.create_all(engine)


def main():
    user = User(username="ymdmzk1999", password="Test123", email="ymdmzk@jahoo.co.jp")

    ssess.add(user)
    ssess.commit()


if __name__ == "__main__":
    main()
