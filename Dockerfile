FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /RDI

# Install system dependencies
RUN apt-get update --fix-missing && apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libmagic-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the Django project to the container
COPY . .

# Expose the application port
EXPOSE 8000

# Default command (migrations and server run handled by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
