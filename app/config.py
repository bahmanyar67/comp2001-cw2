import os
import urllib.parse

class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mssql+pyodbc:///?odbc_connect="
        "Driver={ODBC Driver 18 for SQL Server};"
        f"Server=tcp:{os.getenv('DATABASE_SERVER')},{os.getenv('DATABASE_PORT')};"
        f"Database={os.getenv('DATABASE_NAME')};"
        f"Uid={os.getenv('DATABASE_USER')};"
        f"Pwd={urllib.parse.quote_plus(os.getenv('DATABASE_PASSWORD'))};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


print(Config.SQLALCHEMY_DATABASE_URI)
