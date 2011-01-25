#!/bin/bash

# "-cmin +180" depends on run-time of 03:30AM

archivedir="/home/archive"
gzdir=`date -d "1 day ago" +"%Y-%m"`

find $archivedir -type f -not -name '*.gz' -cmin +180 -size 0 | xargs -r rm

find $archivedir -type f -not -name '*.gz' -cmin +180 | xargs -r gzip

find $archivedir -maxdepth 1 -mindepth 1 -type d | while read category ; do
    if [ ! -d $category/$gzdir ]; then
        mkdir $category/$gzdir
    fi
    ptn="$category/*.gz"
    if [ x"$(echo $ptn)" != x"$ptn" ]; then
        mv $category/*.gz $category/$gzdir
    fi
done

