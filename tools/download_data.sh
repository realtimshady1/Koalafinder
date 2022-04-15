#!/bin/sh
NAME="tmp.rar"
echo "Start download..."
while read ID FILE; do
    CMD=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://docs.google$
    wget -nv --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=${CMD}&id=${ID}" -O ${NAME} $
    echo "Downloading $FILE..."
    mkdir $FILE
    unrar e $NAME -idq -y $FILE
done < "../gdrive_ids.txt"
echo "Download Complete."
rm $NAME
