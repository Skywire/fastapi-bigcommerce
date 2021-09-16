import os

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{os.getcwd()}/{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)