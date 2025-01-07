# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables to avoid buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ACCEPT_EULA=Y
# Set the working directory
WORKDIR /app

# install system dependencies
RUN apt-get update -y && apt-get update \
  && apt-get install -y --no-install-recommends curl gcc g++ gnupg unixodbc-dev libgssapi-krb5-2

# Install system dependencies, including Microsoft ODBC 18 driver
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc |  gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends --allow-unauthenticated msodbcsql18 mssql-tools18 && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile && \
    echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the requirements file first (to leverage Docker cache)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Expose the port your app runs on
EXPOSE 8000

# Set ENTRYPOINT
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["python", "run.py"]