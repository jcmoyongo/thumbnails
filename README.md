# Thumbnails
Creates thumbnails of a given JPEG image.
🐳 Python Docker Project
A lightweight, containerized Python application built for easy deployment and local development.

## Technical Stack

- **Main Language**: Python
- **Dependency Management**: `requirements.txt` (pip)
- **Key Python Libraries**:
  - Pillow (image processing)
  - aiohttp, asyncio (asynchronous operations)
  - requests (HTTP requests)
  - msal (Microsoft authentication)
- **Infrastructure as Code**: Terraform (`.tf`)
  - Azure Resource Manager (azurerm)
  - random provider
- **Containerization**:
  - Docker (`Dockerfile`, `docker-compose.yml`, `docker-compose.debug.yml`)
- **Orchestration**:
  - Docker Compose
  - Kubernetes Job (`deployment.yaml`)
- **Cloud**:
  - Azure Storage
  - Azure Container Registry
  - Azure Container Apps
- **CI/CD & Deployment**:
  - YAML files for deployment
- **Other**:
  - Docker volumes for persistence
  - Environment and access management via MSAL

📦 Features
- Containerized with Docker for platform independence
- Python 3.13.5 with modular script design
- VSCode integration for seamless editing and debugging
- Async task handling, thumbnail generation, etc.

  
Build and Run
# Build Docker image
docker build -t thumb_nails .
# Run the container
 docker run -it -v /c/Users/you/thumb_nails:/mnt/thumb_nails --entrypoint /bin/bash thumb_nails                                                                     


If using Docker Compose:
docker-compose up

🏅 Badges

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)![Docker](https://img.shields.io/badge/Dockerized-%F0%9F%90%AB-blue?logo=docker) ![License](https://img.shields.io/github/license/jcmoyongo/thumbnails) 
![Last Commit](https://img.shields.io/github/last-commit/jcmoyongo/thumbnails) ![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Issues](https://img.shields.io/github/issues/jcmoyongo/thumbnails)

