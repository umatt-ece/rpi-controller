#!/bin/bash

# Check if docker is installed
if ! docker -v >/dev/null ; then
  echo "Docker is not installed on your system."
  # Prompt the user to install Docker and Docker Compose
  while true; do
    read -r -p "Would you like to install Docker? (y/n): " choice
    case $choice in
      [Yy])
        sudo apt update
        sudo apt install -y docker docker-compose
        break
        ;;
      [Nn])
        echo "Skipping Docker and Docker Compose installation."
        break
        ;;
      *)
        echo "Please enter 'y' or 'n'."
        ;;
    esac
  done
fi

# Run Python script to generate docker-compose files
python3 ./scripts/generate_docker_compose_files.py Linux
