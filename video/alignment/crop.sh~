#!/bin/csh -f

# Daniel Scharstein 2017

if ($#argv < 2) then
  echo "usage: extractframes file.mp4 framedir"
  echo ""
  echo "saves frames in framedir/frame%04d.jpg"
  echo ""
  exit 1
endif

# -q:v 1 option means with highest quality

mkdir -p $2
ffmpeg -i $1 -q:v 1 -start_number 0 $2/frame%04d.jpg
echo "created directory $2"
