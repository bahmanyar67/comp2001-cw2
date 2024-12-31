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
            user_email NVARCHAR(255) NOT NULL UNIQUE,
            user_role NVARCHAR(50) NOT NULL
        );
    END
    """)

    trail_table_sql = ("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'trails' AND schema_id = SCHEMA_ID('""" + os.getenv("DATABASE_SCHEMA_NAME") + """'))
    BEGIN
        CREATE TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[trails] (
            trail_id INT PRIMARY KEY IDENTITY(1,1),
            trail_name NVARCHAR(100) NOT NULL,
            trail_summary NVARCHAR(MAX) NOT NULL,
            trail_description NVARCHAR(MAX),
            trail_owner_id INT NOT NULL,
            trail_route_type_id TINYINT NOT NULL,
            trail_surface_type_id TINYINT NOT NULL,
            trail_location_id SMALLINT NOT NULL,
            trail_street NVARCHAR(255),
            trail_postal_code NVARCHAR(20),
            trail_county_id TINYINT,
            trail_city NVARCHAR(100),
            trail_length DECIMAL(5,2) NOT NULL,
            trail_length_unit NVARCHAR(20),
            trail_elevation_gain DECIMAL(5,2),
            trail_elevation_gain_unit NVARCHAR(20),
            trail_starting_point_lat DECIMAL(9,6),
            trail_starting_point_long DECIMAL(9,6),
            trail_ending_point_lat DECIMAL(9,6),
            trail_ending_point_long DECIMAL(9,6),
            trail_difficulty NVARCHAR(50),
            trail_created_at DATETIME DEFAULT GETDATE(),
            trail_updated_at DATETIME DEFAULT GETDATE(),
            FOREIGN KEY (trail_owner_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[users](user_id),
            FOREIGN KEY (trail_route_type_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[route_types](route_type_id),
            FOREIGN KEY (trail_surface_type_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[surface_types](surface_type_id),
            FOREIGN KEY (trail_location_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[locations](location_id),
            FOREIGN KEY (trail_county_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[counties](county_id)
        );
    END
    """)

    trail_tag_table_sql = ("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'trail_tag' AND schema_id = SCHEMA_ID('""" + os.getenv("DATABASE_SCHEMA_NAME") + """'))
    BEGIN
        CREATE TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[trail_tag] (
            trail_id INT NOT NULL,
            tag_id INT NOT NULL,
            PRIMARY KEY (trail_id, tag_id),
            FOREIGN KEY (trail_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[trails](trail_id),
            FOREIGN KEY (tag_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[tags](tag_id)
        );
    END
    """)

    execute_query(county_table_sql)
    execute_query(location_table_sql)
    execute_query(surface_type_table_sql)
    execute_query(route_types_table_sql)
    execute_query(tag_table_sql)
    execute_query(user_table_sql)
    execute_query(trail_table_sql)
    execute_query(trail_tag_table_sql)

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
