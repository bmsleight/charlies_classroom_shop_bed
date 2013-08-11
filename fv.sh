#!/bin/bash
#

rm new-frames/*
rm s_frames.mpg

for f in frame*.png
do
        echo " " | convert -size 1615x765 xc:gray10  -pointsize 24 -fill White -gravity SouthWest  -annotate +766-16 '@-'   jpg:- | convert -  -gravity center \( $f -resize 920x \)   -geometry +4+4 -gravity NorthWest  -composite  \( model_as_seen_webcam.png -resize 640x \) -geometry +4+4 -gravity NorthEast  -composite  -flatten  new-frames/$f.jpg 
        echo $f
done

#cat monts/*.jpg | ffmpeg -f image2pipe -r 15 -vcodec mjpeg -i - -vcodec mpeg4 -s 1280x720 -b 2M out.mp4
#cat monts/*.jpg | ffmpeg -f image2pipe -r 15 -vcodec mjpeg -i - -vcodec mpeg4 -s 720x576 -b 2M out.mp4
cat new-frames/*.jpg | ffmpeg -f image2pipe -r 15 -vcodec mjpeg -i - -target pal-dvd  s_frames.mpg
#\( $f -resize 640x480 \)
