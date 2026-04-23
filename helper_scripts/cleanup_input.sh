#!/bin/bash

# Loop through all .wav and .TextGrid files in the directory
for file in *.{wav,TextGrid}; do
  # Skip if the glob doesn't match any files (prevents errors)
  [ -e "$file" ] || continue

  # Extract everything before the first dot (e.g., "1_pop")
  prefix="${file%%.*}"

  # Extract the file extension (e.g., "wav" or "TextGrid")
  extension="${file##*.}"

  # Piece them back together
  new_file="${prefix}.${extension}"

  # Rename the file (only if the name is actually changing)
  if [ "$file" != "$new_file" ]; then
    mv "$file" "$new_file"
    echo "Renamed: '$file' -> '$new_file'"
  fi
done
