#!/bin/sh

if [ $# -eq 2 ] 
then
	mkdir $2
	ffmpeg -i $1 -vf "select=not(mod(n\,5))" -vsync vfr -qscale:v 2 -start_number 0 $2/%05d.jpg
elif [ $# -eq 4 ] 
then
	ENUM_LARGEST=$(ls obj | sed 's/^0*//' | sed 's/.jpg//' | sed 's/.txt//' | sort -n | tail -1)
	if [ -z "$ENUM_LARGEST" ]
	then
		ENUM_LARGEST = 0
	fi
	mkdir $2
	ffmpeg -ss $3 -to $4 -i $1 -vf "select=not(mod(n\,5))" -vsync vfr -qscale:v 2 -start_number $ENUM_LARGEST $2/%05d.jpg
else
	echo "Wrong number of arguments provided"
fi

