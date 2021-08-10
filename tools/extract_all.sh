#!/bin/sh

if [ $# -eq 1 ] 
then
	FOLDER=${1//.MP4}
	mkdir $FOLDER
	COUNT=$(ls $FOLDER | wc -l)
	LIST=$(ls $FOLDER | sed 's/.txt//' | sed 's/^0*//')
	LIST="eq(n\,"${LIST//$'\n'/)+eq(n\\,}")"
	ffmpeg -i $1 -vf "select="$LIST -vsync vfr -q:v 1 -frame_pts 1 $FOLDER/%08d.jpg
	sleep 30
else
	echo "Wrong number of arguments provided."
	sleep 3
fi
echo "Video conversion completed."
sleep 3
