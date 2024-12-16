#!/bin/bash

# Set the maximum size (in KB)
MAX_SIZE=200

# Folder containing the JPG files
FOLDER="photos"

# Loop through each JPG file in the folder
for file in "$FOLDER"/*.jpg; do
  # Check if file size exceeds the maximum size
  FILE_SIZE=$(du -k "$file" | cut -f1)
  
  if [ "$FILE_SIZE" -gt "$MAX_SIZE" ]; then
    echo "Compressing: $file (Size: ${FILE_SIZE} KB)"
    
    # Compress the image to reduce its file size
    mogrify -resize 75% -quality 85 "$file"
    
    # Check if the compression succeeded
    NEW_FILE_SIZE=$(du -k "$file" | cut -f1)
    if [ "$NEW_FILE_SIZE" -le "$MAX_SIZE" ]; then
      echo "Successfully compressed: $file (New Size: ${NEW_FILE_SIZE} KB)"
    else
      echo "Further compression needed for: $file (Current Size: ${NEW_FILE_SIZE} KB)"
    fi
  else
    echo "Skipping: $file (Size: ${FILE_SIZE} KB)"
  fi
done
