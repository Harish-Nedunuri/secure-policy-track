#!/bin/bash

# Remove any old versions of Docker
sudo apt-get remove -y docker docker-engine docker.io containerd runc

# Update package lists
sudo apt-get update -y

# Install dependencies
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Create the directory for keyrings if it doesn't exist
sudo mkdir -p /etc/apt/keyrings

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list

sudo apt-get install docker-ce docker-ce-cli containerd.io 
sudo apt  install docker-compose