# Use the official Python 3.13.1 base image
FROM python:3.13.1-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt /app/requirements.txt

# Install system dependencies and Python dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc && apt-get autoremove -y && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the application code to the container
COPY . /app

# Expose the default port for Uvicorn
EXPOSE 8002

# Specify the default command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"]
