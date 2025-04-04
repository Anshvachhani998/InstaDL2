#!/bin/bash

# Folder Name
DIR="InstaDL"

# Check if the folder exists
if [ -d "$DIR" ]; then
    echo "📂 $DIR found. Entering directory..."
    cd $DIR || exit 1
else
    echo "❌ $DIR not found! Running commands in the current directory..."
fi

# Pull the latest updates
echo "🔄 Updating repository..."
sudo git pull origin main

# Restart Docker Container
echo "🚀 Restarting YouTubeDL Docker container..."
sudo docker restart YouTubeDL

echo "✅ Update & Restart Completed!"
