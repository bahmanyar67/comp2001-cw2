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
            IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'locations' AND schema_id = SCHEMA_ID('""" + os.getenv(
        "DATABASE_SCHEMA_NAME") + """'))
            BEGIN
                CREATE TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[locations] (
                    location_id SMALLINT PRIMARY KEY IDENTITY(1,1),
                    location_name NVARCHAR(100) NOT NULL,
                );
            END
        """)

    surface_type_table_sql = ("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'surface_types' AND schema_id = SCHEMA_ID('""" + os.getenv(
        "DATABASE_SCHEMA_NAME") + """'))
    BEGIN
        CREATE TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[surface_types] (
            surface_type_id TINYINT PRIMARY KEY IDENTITY(1,1),
            surface_type_name NVARCHAR(100) NOT NULL
        );
    END
    """)

    route_types_table_sql = ("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'route_types' AND schema_id = SCHEMA_ID('""" + os.getenv(
        "DATABASE_SCHEMA_NAME") + """'))
    BEGIN
        CREATE TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[route_types] (
            route_type_id TINYINT PRIMARY KEY IDENTITY(1,1),
            route_type_name NVARCHAR(100) NOT NULL
        );
    END
    """)

    tag_table_sql = ("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'tags' AND schema_id = SCHEMA_ID('""" + os.getenv(
        "DATABASE_SCHEMA_NAME") + """'))
    BEGIN
        CREATE TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[tags] (
            tag_id INT PRIMARY KEY IDENTITY(1,1),
            tag_name NVARCHAR(100) NOT NULL
        );
    END
    """)

    user_table_sql = ("""
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'users' AND schema_id = SCHEMA_ID('""" + os.getenv(
        "DATABASE_SCHEMA_NAME") + """'))
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
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'trail_tag' AND schema_id = SCHEMA_ID('""" + os.getenv(
        "DATABASE_SCHEMA_NAME") + """'))
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
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'coordinates' AND schema_id = SCHEMA_ID('""" + os.getenv(
        "DATABASE_SCHEMA_NAME") + """'))
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
    IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'logs' AND schema_id = SCHEMA_ID('""" + os.getenv(
        "DATABASE_SCHEMA_NAME") + """'))
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
    trail_details_view_sql = f"""
            IF NOT EXISTS (SELECT * FROM sys.views WHERE name = 'trail_details' AND schema_id = SCHEMA_ID('{os.getenv("DATABASE_SCHEMA_NAME")}'))
            BEGIN
                EXEC('
                    CREATE VIEW [{os.getenv("DATABASE_SCHEMA_NAME")}].[trail_details] AS
                    SELECT
                        t.trail_id,
                        t.trail_name,
                        t.trail_summary,
                        t.trail_description,
                        u.user_name AS trail_owner,
                        rt.route_type_name AS trail_route_type,
                        t.trail_surface_type_id,
                        st.surface_type_name AS trail_surface_type,
                        l.location_name AS trail_location,
                        t.trail_street,
                        t.trail_postal_code,
                        c.county_name AS trail_county,
                        t.trail_city,
                        t.trail_length,
                        t.trail_length_unit,
                        t.trail_elevation_gain,
                        t.trail_elevation_gain_unit,
                        t.trail_starting_point_lat,
                        t.trail_starting_point_long,
                        t.trail_ending_point_lat,
                        t.trail_ending_point_long,
                        t.trail_difficulty,
                        t.trail_created_at,
                        t.trail_updated_at,
                        STRING_AGG(tag.tag_name, '', '') AS tags,
                        STRING_AGG(CONCAT(coord.latitude, '', '', coord.longitude), '', '') AS coordinates

                    FROM
                        [{os.getenv("DATABASE_SCHEMA_NAME")}].[trails] t
                    LEFT JOIN
                        [{os.getenv("DATABASE_SCHEMA_NAME")}].[users] u ON t.trail_owner_id = u.user_id
                    LEFT JOIN
                        [{os.getenv("DATABASE_SCHEMA_NAME")}].[route_types] rt ON t.trail_route_type_id = rt.route_type_id
                    LEFT JOIN
                        [{os.getenv("DATABASE_SCHEMA_NAME")}].[surface_types] st ON t.trail_surface_type_id = st.surface_type_id
                    LEFT JOIN
                        [{os.getenv("DATABASE_SCHEMA_NAME")}].[locations] l ON t.trail_location_id = l.location_id
                    LEFT JOIN
                        [{os.getenv("DATABASE_SCHEMA_NAME")}].[counties] c ON t.trail_county_id = c.county_id
                    LEFT JOIN
                        [{os.getenv("DATABASE_SCHEMA_NAME")}].[trail_tag] tt ON t.trail_id = tt.trail_id
                    LEFT JOIN
                        [{os.getenv("DATABASE_SCHEMA_NAME")}].[tags] tag ON tt.tag_id = tag.tag_id
                    LEFT JOIN
                        [{os.getenv("DATABASE_SCHEMA_NAME")}].[coordinates] coord ON t.trail_id = coord.trail_id
                    GROUP BY
                        t.trail_id, t.trail_name, t.trail_summary, t.trail_description, t.trail_owner_id, u.user_name,
                        t.trail_route_type_id, rt.route_type_name, t.trail_surface_type_id, st.surface_type_name,
                        t.trail_location_id, l.location_name, t.trail_street, t.trail_postal_code, t.trail_county_id,
                        c.county_name, t.trail_city, t.trail_length, t.trail_length_unit, t.trail_elevation_gain,
                        t.trail_elevation_gain_unit, t.trail_starting_point_lat, t.trail_starting_point_long,
                        t.trail_ending_point_lat, t.trail_ending_point_long, t.trail_difficulty, t.trail_created_at,
                        t.trail_updated_at
                ')
            END
        """
    execute_query(trail_details_view_sql)


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

    # Trails
    trails_data = [
        (
            "Dartmoor National Park",
            "Dartmoor is a vast moorland in the county of Devon, in southwest England. Dartmoor National Park is known for its rugged terrain, medieval villages and granite tors (rock outcrops). The park also shelters prehistoric ruins including the stone rows and circles of Grey Wethers and Beardown Tors. Ponies roam its craggy landscape, defined by forests, rivers, wetlands and tors.",
            1, 1, 1, 1, "Dartmoor National Park, Devon", "PL20 6SG", 1, "Princetown", 954.00, "km", 621.00, "m", 50.571,
            -3.992, 50.571, -3.992, "Moderate",
            [3, 5, 2], [(50.571, -3.992), (50.571, -3.992), (50.571, -3.992)]
        ),
        (
            "Exmoor National Park",
            "Exmoor National Park is a national park situated in the counties of Devon and Somerset, in South West England. The park covers 267 square miles (690 km2) of hilly open moorland, and includes the Brendon Hills, the East Lyn Valley, the Vale of Porlock and 55 km (34 mi) of the Bristol Channel coast.",
            2, 2, 2, 2, "Exmoor National Park, Devon", "TA24 7SH", 2, "Dulverton", 692.00, "km", 623.00, "m", 51.165,
            -3.825, 51.165, -3.825, "Moderate",
            [1, 4, 5], [(51.165, -3.825), (51.165, -3.825), (51.165, -3.825)]
        ),
        (
            "Lake District National Park",
            "The Lake District, also known as the Lakes or Lakeland, is a mountainous region in North West England. A popular holiday destination, it is famous for its lakes, forests and mountains (or fells), and its associations with William Wordsworth and other Lake Poets and also with Beatrix Potter and John Ruskin.",
            3, 3, 3, 3, "Lake District National Park, Cumbria", "CA12 5XN", 3, "Keswick", 978.00, "km", 912.00, "m",
            54.460, -3.088, 54.460, -3.088, "Moderate",
            [1, 2], [(54.460, -3.088), (54.460, -3.088), (54.460, -3.088)]
        )
    ]

    for trail in trails_data:
        trail_insert_sql = f"""
                IF NOT EXISTS (SELECT * FROM [{os.getenv("DATABASE_SCHEMA_NAME")}].[trails] WHERE trail_name = '{trail[0]}')
                BEGIN
                    INSERT INTO [{os.getenv("DATABASE_SCHEMA_NAME")}].[trails] (
                        trail_name, trail_summary, trail_owner_id, trail_route_type_id, trail_surface_type_id, trail_location_id,
                        trail_street, trail_postal_code, trail_county_id, trail_city, trail_length, trail_length_unit,
                        trail_elevation_gain, trail_elevation_gain_unit, trail_starting_point_lat, trail_starting_point_long,
                        trail_ending_point_lat, trail_ending_point_long, trail_difficulty
                    )
                    VALUES (
                        '{trail[0]}', '{trail[1]}', {trail[2]}, {trail[3]}, {trail[4]}, {trail[5]},
                        '{trail[6]}', '{trail[7]}', {trail[8]}, '{trail[9]}', {trail[10]}, '{trail[11]}',
                        {trail[12]}, '{trail[13]}', {trail[14]}, {trail[15]}, {trail[16]}, {trail[17]}, '{trail[18]}'
                    )
                END
            """
        execute_query(trail_insert_sql)

        # Retrieve the trail_id of the newly inserted trail
        cursor.execute(
            f"SELECT trail_id FROM [{os.getenv('DATABASE_SCHEMA_NAME')}].[trails] WHERE trail_name = '{trail[0]}'")
        trail_id = cursor.fetchone()[0]

        # Insert tags
        for tag in trail[19]:
            tag_insert_sql = f"""
                   INSERT INTO [{os.getenv('DATABASE_SCHEMA_NAME')}].[trail_tag] (trail_id, tag_id)
                   VALUES ({trail_id}, {tag})
               """
            execute_query(tag_insert_sql)

        # Insert coordinates
        for coordinate in trail[20]:
            coordinate_insert_sql = f"""
                   INSERT INTO [{os.getenv('DATABASE_SCHEMA_NAME')}].[coordinates] (trail_id, latitude, longitude)
                   VALUES ({trail_id}, {coordinate[0]}, {coordinate[1]})
               """
            execute_query(coordinate_insert_sql)


    print("Default data created successfully")


# 6. Drop Tables
def drop_tables():
    print("Dropping tables...")
    tables = [
        "coordinates",
        "logs",
        "trail_tag",
        "trails",
        "users",
        "tags",
        "route_types",
        "surface_types",
        "locations",
        "counties"
    ]

    for table in tables:
        drop_table_sql = ("""
            IF EXISTS (SELECT * FROM sys.tables WHERE name = '""" + table + """' AND schema_id = SCHEMA_ID('""" + os.getenv(
            "DATABASE_SCHEMA_NAME") + """'))
            BEGIN
                DROP TABLE [""" + os.getenv("DATABASE_SCHEMA_NAME") + """].[""" + table + """]
            END
            """)
        execute_query(drop_table_sql)

    print("Tables dropped successfully")


# refresh database
def refresh_database():
    print("Refreshing the database...")
    drop_tables()
    # drop_views()
    # drop_stored_procedures()
    # drop_default_data()
    print("Database refresh complete.")


def initialize_database():
    # refresh_database()
    print("Initializing the database...")
    # create_schema(os.getenv("DATABASE_SCHEMA_NAME"))
    # create_tables()
    create_views()
    # create_stored_procedures()
    # create_default_data()
    print("Database initialization complete.")


# Run the initialization
if __name__ == "__main__":
    initialize_database()

# Close the connection
cursor.close()
connection.close()
