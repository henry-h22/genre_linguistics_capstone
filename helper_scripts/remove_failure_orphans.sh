#!/bin/bash

# Loop through all .wav files in the directory
for wav_file in *.wav; do
  # Skip if the glob doesn't match any files
  [ -e "$wav_file" ] || continue

  # Extract the base name by stripping the ".wav" extension
  base_name="${wav_file%.wav}"

  # Define the expected matching TextGrid filename
  textgrid_file="${base_name}.TextGrid"

  # Check if the matching TextGrid file does NOT exist
  if [ ! -f "$textgrid_file" ]; then
    echo "No matching TextGrid for: '$wav_file' -> Deleting..."
    rm "$wav_file"
  fi
done