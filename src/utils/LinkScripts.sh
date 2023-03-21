#!/bin/bash

# Set the source directory and the target directory

script_path=$(readlink -f "$0")
script_directory=$(dirname $(dirname $(dirname "$script_path")))
src_directory="$script_directory/src/cli"
target_directory="/usr/local/bin"
symlink_target="$script_directory/src/utils/runInCD"

# Loop through all .py files in the src_directory
for file in "$src_directory"/*.py; do
    # Get the filename without the .py extension
    filename=$(basename "$file" .py)
    
    # Remove the existing symlink in the target_directory, if it exists
    sudo rm -i "$target_directory/$filename"
    
    # Create the new symlink in the target_directory
    sudo ln -s "$symlink_target" "$target_directory/$filename"
done

