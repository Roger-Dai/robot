#!/bin/csh -f

if ($#argv < 1) then
  echo "usage: crop file.jpg"
  echo ""
  exit 1
endif

convert $1 -crop 1918x3410+553+311 +repage -resize 1080x1920 $1-cropped.jpg

#convert $1 -crop 3410x1918+311+553 +repage -resize 1920x1080 $1-cropped.jpg
