#!/bin/sh 
cd `dirname $0`
. ./venv/bin/activate
python3 src/s3backup.py $@
