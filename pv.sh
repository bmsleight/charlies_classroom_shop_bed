#!/bin/bash
#

rm monts/*
rm out.mp4

for f in images/fishchuck___*
do
        rc_filename=$(echo $f | sed s/fish/room/)
        fc_filename=$(basename "$f")
        c_filename="${fc_filename%.*}"
        plain_filename=$(echo $c_filename | sed s/fishchuck__//)
	text=$(echo $c_filename | sed s/fishchuck___// | sed s/_/\ /)
	echo $fc_filename $rc_filename $text
        convert -background black -fill white  -gravity SouthWest -size 1920x1080 -pointsize 48 -geometry +200-200 label:" $text" tmp.jpg 
#	convert tmp.jpg -composite $rc_filename -gravity NorthWest  -composite $f -gravity SouthEast  monts/montage__$plain_filename.jpg 
	convert tmp.jpg  -gravity center $rc_filename -gravity NorthWest  -composite $f -gravity SouthEast  -composite  monts/montage__$plain_filename.jpg 

done

cat monts/*.jpg | ffmpeg -f image2pipe -r 15 -vcodec mjpeg -i - -vcodec mpeg4 -s 1280x720 -b 2M out.mp4
