#!/bin/sh


if [ $# -eq 1 ] 
then
	FOLDER=${1//.MP4}
	mkdir $FOLDER
	ffmpeg -i $1 -vf "select=not(mod(n\,5))" -vsync vfr -qscale:v 2 -start_number 0 $FOLDER/${FOLDER}_%05d.jpg
elif [ $# -eq 3 ] 
then
	FOLDER=${1//.MP4}
	mkdir $FOLDER
	ENUM_LARGEST=$(ls $FOLDER | sed 's/.jpg//' | sed 's/.txt//' | tail -c 5 | sed 's/^0*//' | sort -n | tail -1)
	if [ -z "$ENUM_LARGEST" ]
	then
		ENUM_LARGEST=0
	fi
	ffmpeg -ss $2 -to $3 -i $1 -vf "select=not(mod(n\,5))" -vsync vfr -qscale:v 2 -start_number $ENUM_LARGEST $FOLDER/${FOLDER}_%05d.jpg
	echo $FOLDER
else
	echo "Wrong number of arguments provided."
	wait 3
fi
echo "Video conversion completed."
echo "Creating template for image labels..."

cd $FOLDER
for name in $(ls | grep .jpg | sed 's/.jpg//')
do
	if [ ! -f $name.txt ]
	then
		touch "$name.txt"
	fi
done