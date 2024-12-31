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

```bash
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
docker pull mohamedelkadi/trail-rest-api
```
