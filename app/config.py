import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

config = {
    "CLIENT_SECRET": os.getenv('CLIENT_SECRET'),
    "CLIENT_ID": os.getenv('CLIENT_ID'),
    "FRONTEND_URL": os.getenv('FRONTEND_URL'),
    "DATABASE_URL": os.getenv('DATABASE_URL'),
}