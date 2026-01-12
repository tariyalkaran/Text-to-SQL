# Use a lightweight Python image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies and ODBC Driver 18
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gnupg \
    unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    mkdir -p /opt/microsoft/msodbcsql18 && \
    echo "ACCEPT_EULA=Y" > /opt/microsoft/msodbcsql18/ACCEPT_EULA && \
    apt-get install -y msodbcsql18 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency list
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Expose Streamlit’s port
EXPOSE 9401

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=9401
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Command to start the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=9401", "--server.address=0.0.0.0"]