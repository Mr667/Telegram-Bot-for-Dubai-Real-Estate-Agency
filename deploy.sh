#!/bin/bash
# deploy.sh
# Deployment script for Ubuntu/Debian server using Docker

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting Deployment for Bayut Telegram Bot..."

# Check if docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker could not be found. Installing docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm get-docker.sh
    echo "Docker installed successfully."
fi

# Make sure .env exists
if [ ! -f .env ]; then
    echo "WARNING: .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "Please update the .env file with your real credentials before running the bot."
    exit 1
fi

# Build Docker image
echo "Building Docker image..."
docker build -t bayut-bot:latest .

# Stop existing container if it's running
if [ $(docker ps -q -f name=bayut-bot_container) ]; then
    echo "Stopping existing bot container..."
    docker stop bayut-bot_container
    docker rm bayut-bot_container
fi

# Run the new container
echo "Starting new bot container..."
docker run -d --name bayut-bot_container --restart unless-stopped -v $(pwd)/.env:/app/.env bayut-bot:latest

echo "Deployment complete! The bot is now running in the background."
echo "Use 'docker logs -f bayut-bot_container' to view logs."
