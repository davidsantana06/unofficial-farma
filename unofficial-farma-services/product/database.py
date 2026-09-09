from sqlmodel import Session, create_engine
import os

engine = create_engine(os.environ["DATABASE_URL"])


def get_session():
    with Session(engine) as session:
        yield session
