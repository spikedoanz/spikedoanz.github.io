#!/bin/bash

# Set the source and destination directory paths
source_dir=~/Global/Vault/work/website/content
dest_dir=.

rm -rf content

npx quartz build --serve &

while true; do
    cp -r "$source_dir" "$dest_dir"
    sleep 5
done
