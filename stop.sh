#!/bin/bash

echo "***"
echo "*** Stopping application"
echo "***"
sudo pkill -f rest_api.py

echo "***"
echo "*** Stopping virtualenv"
echo "***"
deactivate

echo "***"
echo "*** Deleting temp files"
echo "***"
sudo rm *.pyc
sudo rm -r ./env
sudo rm -r ./log
sudo rm ./model_mf2c/*.pyc
sudo rm -r ./src/stubs
sudo rm ./src/*.pyc
