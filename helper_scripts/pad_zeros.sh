#!/bin/bash

# Loop through all files in the directory
for file in *; do
  # Skip directories or things that aren't regular files
  [ -f "$file" ] || continue

  # Extract the part BEFORE the first underscore (the number)
  number="${file%%_*}"

  # Check to make sure we actually grabbed a number 
  # (this prevents the script from accidentally renaming itself or other files)
  if [[ "$number" =~ ^[0-9]+$ ]]; then
    
    # Extract the part AFTER the first underscore (e.g., "pop.wav" or "pop.TextGrid")
    rest="${file#*_}"

    # Pad the number with leading zeros to make it exactly 3 digits long
    # The "10#" forces bash to treat the number as base-10, preventing weird errors
    padded_number=$(printf "%03d" "$((10#$number))")

    # Piece the filename back together
    new_file="${padded_number}_${rest}"

    # Rename if the name actually needs changing
    if [ "$file" != "$new_file" ]; then
      mv "$file" "$new_file"
      echo "Renamed: '$file' -> '$new_file'"
    fi
  fi
done