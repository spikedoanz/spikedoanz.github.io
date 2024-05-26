#!/bin/bash

# Set the source and destination directory paths
source_dir=~/Global/Vault/website/content
dest_dir=.

npx quartz build --serve &

while true; do
    cp -r "$source_dir" "$dest_dir"
    sleep 5
done
