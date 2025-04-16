#!/bin/bash

# Set the directory containing the PNG files
directory="."

# Loop over all PNG files in the directory
for file in "$directory"/*.png; do
    if [ -f "$file" ]; then
        # Extract the filename without the path
        filename=$(basename "$file")

        # Extract pieces between exactly two "__" substrings
        pieces=($(echo "$filename" | awk -F'__' '{for (i=2; i<=NF-1; i++) print $i}'))

        # Create folder structure
        current_path="$directory"
        for piece in "${pieces[@]}"; do
            current_path="$current_path/$piece"
            mkdir -p "$current_path"
        done

        # Move the PNG file to the created folder
        mv "$file" "$current_path/"

        # Extract the last piece after the last "__"
        last_piece=$(echo "$filename" | awk -F'__' '{print $NF}')

        # Rename the PNG file
        new_filename="$current_path/$last_piece"
        mv "$current_path/$filename" "$new_filename"

        echo "Moved and renamed: $new_filename"
    fi
done

# Find the last level of subfolders and copy index.php to each
find "$directory" -type d -links 2 -exec cp "index.php" {} \;
echo "Copied index.php to the last level of subfolders."


