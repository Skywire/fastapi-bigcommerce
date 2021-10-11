import os

from sqlmodel import create_engine

from app.config import config

if 'DATABASE_URL' in config and config['DATABASE_URL'] is not None:
    db_url = config['DATABASE_URL']
    db_url = db_url.replace("postgres://", "postgresql://", 1)
else:
    db_url = f"sqlite:///{os.getcwd()}/database.db"

engine = create_engine(db_url, echo=True)
