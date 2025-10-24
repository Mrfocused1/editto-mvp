#!/bin/bash

# Build and push Docker image to Docker Hub or RunPod's container registry

# Configuration
IMAGE_NAME="editto-worker"
TAG="latest"
DOCKER_USERNAME="paulshono"

# Build the image
echo "Building Docker image..."
docker build -t $DOCKER_USERNAME/$IMAGE_NAME:$TAG .

# Push to Docker Hub
echo "Pushing to Docker Hub..."
docker push $DOCKER_USERNAME/$IMAGE_NAME:$TAG

echo "Done! Image: $DOCKER_USERNAME/$IMAGE_NAME:$TAG"
echo "Use this image URL when creating your RunPod endpoint"
