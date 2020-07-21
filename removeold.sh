#!/bin/bash
count=0
files=/home/pranav/mytools/bingwallpapers/*.jpg
boolnone=true
for file in $files ; do
    if [ -a $file -a ! -d $file ]; then
        time=$(ls -lu --time-style=+%s $file | cut -d " " -f 6)
        current=$(date +%s)
        diff=$((current-time))
        readablediff=$(date -u -d @$diff +"%j:%T")
        count=$(expr $count + 1)
        if [ $diff -gt 604800 ]; then
            readabletime=$(date --date="1970-01-01 UTC $time seconds" "+%Y/%m/%d %H:%M")
            echo "Moving file   "$file"-- Dated"$readabletime
            mv $file /home/pranav/mytools/OLD_WALLPAPERS/
            boolnone=false
        fi
    fi
done
if [ "$boolnone" = true ]; then
    echo NONE
fi
