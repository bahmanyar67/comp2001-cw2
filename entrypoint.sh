#!/bin/bash

# Check if the database is initialized
if [ ! -f /app/.db_initialized ]; then
    echo "Initializing the database..."
    python /app/app/initialize_database.py  # Specify the full path to the script
    touch /app/.db_initialized
else
    echo "Database already initialized."
fi

# Start the application
exec "$@"