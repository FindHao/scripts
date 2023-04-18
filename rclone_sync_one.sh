#!/bin/bash


cloud_file=${cloud_file:-g:/d2023.md}
cloud_folder=${cloud_file%/*}
local_file=${local_file:-/home/yhao24/d/d2023.md}
shadow_folder=${shadow_folder:-/tmp/}
shadow_file=${shadow_folder}/d2023.md


rclone copy $cloud_file $shadow_folder
# check shadow_file and local_file which one is latest
if [ $shadow_file -nt $local_file ]; then
    # cloud file is newer than local file
    cp $shadow_file $local_file
    echo "copy cloud file to local file"
else
    # local file is equal or newer than cloud file
    # check these two files are same or not
    if ! cmp -s $shadow_file $local_file; then
        # these two files are different
        rclone copy $local_file $cloud_folder
        echo "copy local file to cloud file"
    else
        echo "they are same"
    fi
fi

