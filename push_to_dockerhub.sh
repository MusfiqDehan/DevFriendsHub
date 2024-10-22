#!/bin/bash

# Set your Docker Variables
DOCKER_HUB_USERNAME="musfiqdehan"
FRONTEND_IMAGE_NAME="devfriendshub-frontend"
BACKEND_IMAGE_NAME="devfriendshub-backend"
VERSION="latest"

# Build images
docker-compose build

# Tag the backend image
docker tag $BACKEND_IMAGE_NAME:$VERSION $DOCKER_HUB_USERNAME/$BACKEND_IMAGE_NAME:$VERSION
docker tag $FRONTEND_IMAGE_NAME:$VERSION $DOCKER_HUB_USERNAME/$FRONTEND_IMAGE_NAME:$VERSION

# Push the images to Docker Hub
docker push $DOCKER_HUB_USERNAME/$BACKEND_IMAGE_NAME:$VERSION
docker push $DOCKER_HUB_USERNAME/$FRONTEND_IMAGE_NAME:$VERSION

# ===========PULLING IMAGES AND RUNNING THEM LOCALLY==========#

# # Pull the images
# docker pull musfiqdehan/devfriendshub-backend:latest
# docker pull musfiqdehan/devfriendshub-frontend:latest

# # Run the backend container
# docker run -d -p 5050:5050 musfiqdehan/devfriendshub-backend:latest

# # Run the frontend container
# docker run -d -p 3000:80 musfiqdehan/devfriendshub-frontend:latest