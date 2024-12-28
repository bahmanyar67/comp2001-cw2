from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = (
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server=tcp:{os.getenv('DATABASE_SERVER')},{os.getenv('DATABASE_PORT')};"
        f"Database={os.getenv('DATABASE_NAME')};"
        f"Uid={os.getenv('DATABASE_USER')};"
        f"Pwd={os.getenv('DATABASE_PASSWORD')};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
