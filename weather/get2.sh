#!/bin/sh

wget -O map.jpg https://dsx.weather.com/util/image/map/europe_sat_1280x720.jpg

#anytopnm map.jpg | pnmcut 664 106 64 64 | pnmscale 0.5 > lkp.pnm

# lkp 696 138

for z in $(seq 128 -1 32)
do
  anytopnm map.jpg | pnmcut $((696-$z/2)) $((138-$z/2)) $z $z | pnmscale -xysize 32 32 > lkp_$z.pnm
done

