#!/bin/bash

# Pull latest version
git pull

# Build Docker image
docker build -t easyocr-restful .

# Run easyocr restful
docker compose up -d

# Optional, limit resources
docker update --cpus 2 --memory 2048M easyocr-restful

# Optional, view logs
docker logs easyocr-restful -f