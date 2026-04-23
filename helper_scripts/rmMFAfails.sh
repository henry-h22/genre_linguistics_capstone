#!/bin/bash

# Check if the user provided exactly one argument
if [ -z "$1" ]; then
  echo "Error: No source directory provided."
  echo "Usage: ./move_uniques.sh <path_to_Folder_A>"
  exit 1
fi

# Assign the first argument to DIR_A
DIR_A="$1"

# Hardcode the other directories (you can change these to $2 and $3 later if you want!)
DIR_B="/Users/henryheyden/Documents/capstone/GTZAN/topraatsc"
DIR_C="/Users/henryheyden/Documents/capstone/GTZAN/uvr5_out/potpurri2"

# Create Folder C if it doesn't already exist
mkdir -p "$DIR_C"

# Loop through all files in the provided Folder A
for file_a in "$DIR_A"/*; do
  # Skip if it's a directory or if Folder A is empty/invalid
  [ -f "$file_a" ] || continue

  # Extract just the filename
  filename=$(basename "$file_a")

  # Define what the path would be if the file lived in Folder B
  file_b="$DIR_B/$filename"

  # Check if the file does NOT exist in Folder B
  if [ ! -f "$file_b" ]; then
    echo "Unique file found: '$filename'. Moving to '$DIR_C'..."
    cp "$file_a" "$DIR_C/"
  fi
done