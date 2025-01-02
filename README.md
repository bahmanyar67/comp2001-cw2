# Trail REST API

This is a REST API for the Trail application. The API is built using Flask.

## Installation

### From source

1. Clone the repository
2. install the required packages:

```bash
pip install -r requirements.txt
```

3. Install the Microsoft ODBC 18 driver for SQL Server on Mac OS:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql18 mssql-tools18
```

4. Create a `.env` file in the root directory and add the following environment variables:

```dotenv
SECRET_KEY=
DATABASE_SERVER=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_PORT=
DATABASE_SCHEMA_NAME=
```

5. Run the application:

```bash
python app.py
```

### Using Docker

1. pull the image from Docker Hub:

```bash
docker pull bahmanyar67/trail-rest-api
```

2. Create a `.env` file in the root directory and add the following environment variables:

```dotenv
SECRET_KEY=
DATABASE_SERVER=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_PORT=
DATABASE_SCHEMA_NAME=
```

3. Run the container:

```bash
docker run -p 5000:5000 --env-file .env bahmanyar67/trail-rest-api
```

## Usage

To create, update or delete any entity, you need to be logged in as an admin user.
There are two types of users: admin and regular user with the following predefined credentials:

Admin user:
```text
username = grace@plymouth.ac.uk
password = ISAD123!
```

Regular users:
```text
username = tim@plymouth.ac.uk
password = COMP2001!

username = ada@plymouth.ac.uk
password = insecurePassword
```

You can always change the roles of the users in the database through the `/api/v1/users` endpoint.