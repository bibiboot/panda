#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/home/ubuntu/work/motherusc/
export DJANGO_SETTINGS_MODULE=settings
cd /home/ubuntu/work/motherusc
START=$(date +%s)
echo $( date +%T::%m-%d-%Y ) : 'EVENT FB starts'
/usr/bin/python index/readEvents.py >> /home/ubuntu/work/motherusc/logs/fb_event.log
END=$(date +%s)
DIFF=$(( $END - $START ))
echo $( date +%T::%m-%d-%Y ) : 'EVENT FB ends' 'Time-taken = '$DIFF

echo $( date +%T::%m-%d-%Y ) : 'EVENT FB starts'
/usr/bin/python index/readCallis.py >> /home/ubuntu/work/motherusc/logs/fb_event.log
END=$(date +%s)
DIFF=$(( $END - $START ))
echo $( date +%T::%m-%d-%Y ) : 'EVENT FB ends' 'Time-taken = '$DIFF


START=$(date +%s)
echo $( date +%T::%m-%d-%Y ) : 'EVENT INDEX starts'
/usr/bin/python index/events_filler.py >> /home/ubuntu/work/motherusc/logs/index.log
END=$(date +%s)
DIFF=$(( $END - $START ))
echo $( date +%T::%m-%d-%Y ) : 'EVENT INDEX ends' 'Time-taken = '$DIFF

