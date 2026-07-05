FROM python:3.10-slim
WORKDIR /app

# Install the required OS tools for MySQL to talk to Python
RUN apt-get update \
    && apt-get install -y default-libmysqlclient-dev build-essential pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install your Python packages
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your code in
COPY . .

# Expose port 5000 to perfectly match what Caddy is looking for
EXPOSE 5000
