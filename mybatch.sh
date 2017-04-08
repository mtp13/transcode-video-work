#!/usr/bin/env bash

# A function to make words plural by adding an s
# when the value ($2) is != 1 or -1
# It only adds an 's'; it is not very smart.
#
function plural ()
{
    if [ $2 -eq 1 -o $2 -eq -1 ]
    then
        echo ${1}
    else
        echo ${1}s
    fi
}

if [ $# -eq 1 ]
  then
      minutes=$1
      while [ ${minutes} -gt 0 ]; do
          echo "Waiting ${minutes} $(plural "minute" ${minutes}) to proceed ..."
          sleep 60
          let minutes=minutes-1
      done
      echo "Proceeding ..."
fi

readonly work="$(cd "$(dirname "$0")" && pwd)"
readonly queue="$work/queue.txt"
readonly crops="$work/Crops"

input="$(sed -n 1p "$queue")"

while [ "$input" ]; do
    title_name="$(basename "$input" | sed 's/\.[^.]*$//')"
    crop_file="$crops/${title_name}.txt"
    
    if [ -f "$crop_file" ]; then
        crop_option="--crop $(cat "$crop_file")"
    else
        crop_option=''
    fi

    sed -i '' 1d "$queue" || exit 1

    transcode-video --quick --output "/Volumes/Media Disk/transcoded/" $crop_option "$input"

    mv /Volumes/Media\ Disk/transcoded/*.log /Volumes/Media\ Disk/work/log

    input="$(sed -n 1p "$queue")"
done