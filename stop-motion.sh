#!/bin/bash
#


cam1="roomchuck"
cam2="landing"

while true; do
    d=$(date +"%Y-%m-%d_%H-%M-%S")
    suffix="__"$d".jpg"
    wgetjpg1=$cam1"_"$suffix
    wgetjpg2=$cam2"_"$suffix
    mt="montage_"$suffix
    wget -nv http://$cam1:8080/?action=snapshot -O $wgetjpg1
    wget -nv http://$cam2:8080/?action=snapshot -O $wgetjpg2
    montage $wgetjpg1 $wgetjpg2 -geometry 640x480+5+5 $mt
    sleep 3.5
done
