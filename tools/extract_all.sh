#!/bin/sh

if [ $# -eq 1 ] 
then
	FOLDER=${1//.MP4}
	LIST=$(ls $FOLDER | sed 's/.txt//' | sed 's/^0*//')
	LIST="eq(n\,"${LIST//$'\n'/)+eq(n\\,}")"
	ffmpeg -i $1 -vf "select="$LIST -vsync vfr -q:v 1 -frame_pts 1 $FOLDER/%08d.jpg
	sleep 3
elif [ $# -eq 2 ]
then
	LIST=$(ls $2 | head -n 100 | sed 's/.txt//' | sed 's/^0*//')
	LIST="eq(n\,"${LIST//$'\n'/)+eq(n\\,}")"
	ffmpeg -i $1 -vf "select="$LIST -vsync vfr -q:v 1 -frame_pts 1 $2/%08d.jpg
	sleep 3
else
	echo "Wrong number of arguments provided."
	sleep 3
fi
echo "Video conversion completed."
sleep 3
