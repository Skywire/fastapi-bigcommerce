import os

from sqlmodel import create_engine

from app.config import config

if 'DATABASE_URL' in config:
    db_url = config['DATABASE_URL']
else:
    db_url = f"sqlite:///{os.getcwd()}/database.db"

engine = create_engine(db_url, echo=True)
