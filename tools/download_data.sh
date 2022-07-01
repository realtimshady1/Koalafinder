#!/bin/sh
NAME="tmp.rar"
echo "Start download..."
while read ID FILE; do
    CMD=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate "https://docs.google.com/uc?export=download&id=${ID}" -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')
    wget -nv --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=${CMD}&id=${ID}" -O ${NAME} && rm -rf /tmp/cookies.txt
    echo "Downloading $FILE..."
    mkdir $FILE
    unrar e $NAME -idq -y $FILE
done < "../gdrive_ids.txt"
echo "Download Complete."
rm $NAME
