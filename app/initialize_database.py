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
            user_name NVARCHAR(100) NOT NULL,
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
            FOREIGN KEY (trail_owner_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[users](user_id) 
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (trail_route_type_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[route_types](route_type_id)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (trail_surface_type_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[surface_types](surface_type_id)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (trail_location_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[locations](location_id)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (trail_county_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[counties](county_id)
                ON DELETE CASCADE ON UPDATE CASCADE
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
            FOREIGN KEY (trail_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[trails](trail_id)
                ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[tags](tag_id)
                ON DELETE CASCADE ON UPDATE CASCADE
        );
    END
    """)

    coordinates_table_sql = ("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'coordinates' AND schema_id = SCHEMA_ID('""" + os.getenv("DATABASE_SCHEMA_NAME") + """'))
    BEGIN
        CREATE TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[coordinates] (
            coordinate_id INT PRIMARY KEY IDENTITY(1,1),
            trail_id INT NOT NULL,
            latitude DECIMAL(9,6) NOT NULL,
            longitude DECIMAL(9,6) NOT NULL,
            FOREIGN KEY (trail_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[trails](trail_id)
                ON DELETE CASCADE ON UPDATE CASCADE
        );
    END
    """)

    logs_table_sql = ("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'logs' AND schema_id = SCHEMA_ID('""" + os.getenv("DATABASE_SCHEMA_NAME") + """'))
    BEGIN
        CREATE TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[logs] (
            log_id INT PRIMARY KEY IDENTITY(1,1),
            trail_id INT NULL,
            user_id INT NOT NULL,
            action NVARCHAR(200) NOT NULL,
            created_at DATETIME DEFAULT GETDATE(),
            FOREIGN KEY (trail_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[trails](trail_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            FOREIGN KEY (user_id) REFERENCES [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[users](user_id)
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
    execute_query(coordinates_table_sql)
    execute_query(logs_table_sql)

    print("Tables created successfully")


# 3. Create Views
def create_views():
    print("Creating views...")


# 4. Create Stored Procedures
def create_stored_procedures():
    print("Creating stored procedures...")


# 5. Create default Data
def create_default_data():
    # users
    user_data = [
        ("Grace Hopper ", "grace@plymouth.ac.uk", "admin"),
        ("Tim Berners-Lee", "tim@plymouth.ac.uk", "user"),
        ("Ada Lovelace", "ada@plymouth.ac.uk", "user")
    ]

    for user in user_data:
        user_insert_sql = ("""
            IF NOT EXISTS (SELECT * FROM [""" + os.getenv(
            "DATABASE_SCHEMA_NAME") + """].[users] WHERE user_email = '""" + user[1] + """')
            BEGIN
                INSERT INTO [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[users] (user_name, user_email, user_role)
                VALUES ('""" + user[0] + """', '""" + user[1] + """', '""" + user[2] + """')
            END
            """)
        execute_query(user_insert_sql)

    # UK counties
    counties_data = ["Avon", "Bedfordshire", "Berkshire", "Borders", "Buckinghamshire", "Cambridgeshire", "Devon"]
    for county in counties_data:
        county_insert_sql = ("""
            IF NOT EXISTS (SELECT * FROM [""" + os.getenv(
            "DATABASE_SCHEMA_NAME") + """].[counties] WHERE county_name = '""" + county + """')
            BEGIN
                INSERT INTO [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[counties] (county_name)
                VALUES ('""" + county + """')
            END
            """)
        execute_query(county_insert_sql)

    # Locations
    locations_data = ["Dartmoor", "Exmoor", "Lake District", "Peak District", "Snowdonia", "Yorkshire Dales"]
    for location in locations_data:
        location_insert_sql = ("""
            IF NOT EXISTS (SELECT * FROM [""" + os.getenv(
            "DATABASE_SCHEMA_NAME") + """].[locations] WHERE location_name = '""" + location + """')
            BEGIN
                INSERT INTO [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[locations] (location_name)
                VALUES ('""" + location + """')
            END
            """)
        execute_query(location_insert_sql)

    # Surface types
    surface_types_data = ["Asphalt", "Concrete", "Gravel", "Sand", "Dirt", "Rock"]
    for surface_type in surface_types_data:
        surface_type_insert_sql = ("""
            IF NOT EXISTS (SELECT * FROM [""" + os.getenv(
            "DATABASE_SCHEMA_NAME") + """].[surface_types] WHERE surface_type_name = '""" + surface_type + """')
            BEGIN
                INSERT INTO [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[surface_types] (surface_type_name)
                VALUES ('""" + surface_type + """')
            END
            """)
        execute_query(surface_type_insert_sql)

    # Route types
    route_types_data = ["Loop", "Out and back", "Point to point"]
    for route_type in route_types_data:
        route_type_insert_sql = ("""
            IF NOT EXISTS (SELECT * FROM [""" + os.getenv(
            "DATABASE_SCHEMA_NAME") + """].[route_types] WHERE route_type_name = '""" + route_type + """')
            BEGIN
                INSERT INTO [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[route_types] (route_type_name)
                VALUES ('""" + route_type + """')
            END
            """)
        execute_query(route_type_insert_sql)

    # Tags
    tags_data = ["Family friendly", "Dog friendly", "Wheelchair friendly", "Stroller friendly", "Bike friendly"]
    for tag in tags_data:
        tag_insert_sql = ("""
            IF NOT EXISTS (SELECT * FROM [""" + os.getenv(
            "DATABASE_SCHEMA_NAME") + """].[tags] WHERE tag_name = '""" + tag + """')
            BEGIN
                INSERT INTO [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[tags] (tag_name)
                VALUES ('""" + tag + """')
            END
            """)
        execute_query(tag_insert_sql)

    print("Default data created successfully")


# Initialize the database
def initialize_database():
    print("Initializing the database...")
    create_schema(os.getenv("DATABASE_SCHEMA_NAME"))
    create_tables()
    create_views()
    create_stored_procedures()
    create_default_data()
    print("Database initialization complete.")


# Run the initialization
if __name__ == "__main__":
    initialize_database()

# Close the connection
cursor.close()
connection.close()
