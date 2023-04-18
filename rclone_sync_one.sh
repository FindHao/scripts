#!/bin/bash

cloud_file=${cloud_file:-g:/d2023.md}
local_file=${local_file:-/home/yhao24/d/d2023.md}
shadow_file=${shadow_file:-/home/yhao24/d/.d2023.md}

rclone copy $cloud_file $shadow_file
# check shadow_file and local_file which one is latest
if [ $shadow_file -nt $local_file ]; then
    # cloud file is newer than local file
    cp $shadow_file $local_file
else
    rclone copy $local_file $cloud_file
fi

