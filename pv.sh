#!/bin/bash
#

rm monts/*
rm out.mp4
rm out.mpg

#for f in images/fishchuck___*
for f in images/fishchuck___2013-08-05_17-*
#for f in images/fishchuck___2013-08-03_15-23-3*
do
        rc_filename=$(echo $f | sed s/fish/room/)
        fc_filename=$(basename "$f")
        c_filename="${fc_filename%.*}"
        plain_filename=$(echo $c_filename | sed s/fishchuck__//)
        text=$(echo $c_filename | sed s/fishchuck___// | sed s/_/\ / | sed 's/.\{3\}$//')
        echo $fc_filename $rc_filename $text
#        convert -background gray10 -fill white -size 1600x1200  -geometry +100-100 -gravity Northeast  -pointsize 32  label:"$text  \n" jpg:- | convert -  -gravity center $rc_filename -gravity NorthWest  -composite \( $f -resize 640x480 \) -gravity SouthEast  -composite  monts/montage__$plain_filename.jpg 
#         convert -background gray10 -fill white -size 1600x1200 -pointsize 72   -annotate +28+68 'Anthony'    jpg:- | convert -  -gravity center $rc_filename -gravity NorthWest  -composite \( $f -resize 640x480 \) -gravity SouthEast  -composite  monts/montage__$plain_filename.jpg 
        echo $text | convert -size 1615x765 xc:gray10  -pointsize 24 -fill White -gravity SouthWest  -annotate +766-16 '@-'   jpg:- | convert -  -gravity center $rc_filename -gravity NorthWest  -composite \( $f -resize 640x480 \) -gravity NorthEast  -composite  monts/montage__$plain_filename.jpg 

done

#cat monts/*.jpg | ffmpeg -f image2pipe -r 15 -vcodec mjpeg -i - -vcodec mpeg4 -s 1280x720 -b 2M out.mp4
#cat monts/*.jpg | ffmpeg -f image2pipe -r 15 -vcodec mjpeg -i - -vcodec mpeg4 -s 720x576 -b 2M out.mp4
cat monts/*.jpg | ffmpeg -f image2pipe -r 15 -vcodec mjpeg -i - -target pal-dvd  out.mpg
