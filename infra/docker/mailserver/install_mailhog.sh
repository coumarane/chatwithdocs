#!/bin/bash
set -euo pipefail

# Check if Docker is installed
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed. Please install Docker first."
  exit 1
fi

# Pull the latest MailHog image
echo "Pulling MailHog image..."
docker pull mailhog/mailhog:latest

# Check if a container named 'mailhog' already exists
if docker ps -a --format '{{.Names}}' | grep -q '^mailhog$'; then
  echo "MailHog container already exists."
  # Start the container if it's not running
  if ! docker ps --format '{{.Names}}' | grep -q '^mailhog$'; then
    echo "Starting existing MailHog container..."
    docker start mailhog
  else
    echo "MailHog container is already running."
  fi
else
  # Run a new container named 'mailhog' mapping SMTP and web UI ports
  echo "Running a new MailHog container..."
  docker run -d --name mailhog -p 1025:1025 -p 8025:8025 mailhog/mailhog:latest
fi

echo "MailHog is up and running!"
echo "Access the web UI at http://localhost:8025"
