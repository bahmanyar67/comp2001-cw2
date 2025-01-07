import os
from sqlalchemy.engine import URL

class Config:
    SQLALCHEMY_DATABASE_URI = URL.create(
        "mssql+pyodbc",
        username=os.getenv('DATABASE_USER'),
        password=os.getenv('DATABASE_PASSWORD'),
        host=os.getenv('DATABASE_SERVER'),
        port=int(os.getenv('DATABASE_PORT')),
        database=os.getenv('DATABASE_NAME'),
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "Encrypt": "yes",
            "TrustServerCertificate": "yes",
            "Connection Timeout": "30"
        }
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False