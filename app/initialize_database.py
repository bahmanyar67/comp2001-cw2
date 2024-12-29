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

    location_table_sql = ("""
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'locations' AND schema_id = SCHEMA_ID('""" + os.getenv("DATABASE_SCHEMA_NAME") + """'))
            BEGIN
                CREATE TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[locations] (
                    location_id SMALLINT PRIMARY KEY IDENTITY(1,1),
                    location_name NVARCHAR(100) NOT NULL,
                );
            END
        """)

    surface_type_table_sql = ("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'surface_types' AND schema_id = SCHEMA_ID('""" + os.getenv("DATABASE_SCHEMA_NAME") + """'))
    BEGIN
        CREATE TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[surface_types] (
            surface_type_id TINYINT PRIMARY KEY IDENTITY(1,1),
            surface_type_name NVARCHAR(100) NOT NULL
        );
    END
    """)

    route_types_table_sql = ("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'route_types' AND schema_id = SCHEMA_ID('""" + os.getenv("DATABASE_SCHEMA_NAME") + """'))
    BEGIN
        CREATE TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[route_types] (
            route_type_id TINYINT PRIMARY KEY IDENTITY(1,1),
            route_type_name NVARCHAR(100) NOT NULL
        );
    END
    """)

    tag_table_sql = ("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'tags' AND schema_id = SCHEMA_ID('""" + os.getenv("DATABASE_SCHEMA_NAME") + """'))
    BEGIN
        CREATE TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[tags] (
            tag_id INT PRIMARY KEY IDENTITY(1,1),
            tag_name NVARCHAR(100) NOT NULL
        );
    END
    """)

    user_table_sql = ("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users' AND schema_id = SCHEMA_ID('""" + os.getenv("DATABASE_SCHEMA_NAME") + """'))
    BEGIN
        CREATE TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[users] (
            user_id INT PRIMARY KEY IDENTITY(1,1),
            user_email NVARCHAR(255) NOT NULL,
            user_role NVARCHAR(50) NOT NULL
        );
    END
    """)

    execute_query(county_table_sql)
    execute_query(location_table_sql)
    execute_query(surface_type_table_sql)
    execute_query(route_types_table_sql)
    execute_query(tag_table_sql)
    execute_query(user_table_sql)

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
