#!/bin/bash

# "-cmin +180" depends on run-time of 03:30AM

archivedir="/home/archive"
bz2dir=`date -d "1 day ago" +"%Y-%m"`

find $archivedir -type f -not -name '*.gz' -a -not -name '*.bz2' -cmin +180 -size 0 | xargs -r rm

find $archivedir -type f -not -name '*.gz' -a -not -name '*.bz2' -cmin +180 | xargs -r bzip2

find $archivedir -maxdepth 1 -mindepth 1 -type d | while read category ; do
    if [ ! -d $category/$bz2dir ]; then
        mkdir $category/$bz2dir
    fi
    ptn="$category/*.bz2"
    if [ x"$(echo $ptn)" != x"$ptn" ]; then
        mv $category/*.bz2 $category/$bz2dir
    fi
done

