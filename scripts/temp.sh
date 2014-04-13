#!/bin/bash
#. ~/.bashrc

export PYTHONPATH=$PYTHONPATH:/home/ubuntu/work/motherusc/
#export PYTHONPATH='/home/ubuntu/work/motherusc'
export DJANGO_SETTINGS_MODULE=settings
cd /home/ubuntu/work/motherusc
START=$(date +%s)
echo $( date +%T::%m-%d-%Y ) : 'TEMP FB starts'
/usr/bin/python index/readFile.py >> /home/ubuntu/work/motherusc/logs/fb.log
END=$(date +%s)
DIFF=$(( $END - $START ))
echo $( date +%T::%m-%d-%Y ) : 'TEMP FB ends' 'Time-taken = '$DIFF

START=$(date +%s)
echo $( date +%T::%m-%d-%Y ) : 'TEMP INDEX starts'
/usr/bin/python index/temp_filler.py >> /home/ubuntu/work/motherusc/logs/index.log
END=$(date +%s)
DIFF=$(( $END - $START ))
echo $( date +%T::%m-%d-%Y ) : 'TEMP INDEX ends' 'Time-taken = '$DIFF

