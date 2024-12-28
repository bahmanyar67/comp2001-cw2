from dotenv import load_dotenv
import os
import pyodbc

# Load environment variables
load_dotenv()

# Database connection setup
connection_string = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server=tcp:{os.getenv('DATABASE_SERVER')},{os.getenv('DATABASE_PORT')};"
    f"Database={os.getenv('DATABASE_NAME')};"
    f"Uid={os.getenv('DATABASE_USER')};"
    f"Pwd={os.getenv('DATABASE_PASSWORD')};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

# Establish connection
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()


# Function to execute SQL queries
def execute_query(query):
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Exception as e:
        print(f"Error executing query: {e}")
        connection.rollback()


# 1. Create Schema
def create_schema(name):
    # use name parameter to create a schema with a different name
    schema_sql = """
        IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name = '""" + name + """')
        BEGIN
            EXEC('CREATE SCHEMA """ + name + """')
        END
        """
    execute_query(schema_sql)
    print("Schema " + name + " created successfully")


# 2. Create Tables
def create_tables():
    county_table_sql = ("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'counties' AND schema_id = SCHEMA_ID('""" + os.getenv("DATABASE_SCHEMA_NAME") + """'))
            BEGIN
                CREATE TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[counties] (
                    county_id TINYINT PRIMARY KEY IDENTITY(1,1),
                    county_name NVARCHAR(100) NOT NULL
                );
            END
        """)
    execute_query(county_table_sql)

    print("Tables created successfully")


# 3. Create Views
def create_views():
    print("Creating views...")


# 4. Create Stored Procedures
def create_stored_procedures():
    print("Creating stored procedures...")


# Initialize the database
def initialize_database():
    print("Initializing the database...")
    create_schema(os.getenv("DATABASE_SCHEMA_NAME"))
    create_tables()
    print("Database initialization complete.")


# Run the initialization
if __name__ == "__main__":
    initialize_database()

# Close the connection
cursor.close()
connection.close()
