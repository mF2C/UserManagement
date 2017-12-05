#!/bin/bash

sudo bash register.sh

echo "***"
echo "*** Starting virtualenv"
echo "***"
virtualenv env
source env/bin/activate

echo "***"
echo "*** Launching application"
echo "***"
/usr/bin/python2.7 rest_api.py
