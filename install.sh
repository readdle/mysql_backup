#!/bin/sh 
cd `dirname $0`
python3 -m venv venv 
. ./venv/bin/activate
pip3 install boto3

