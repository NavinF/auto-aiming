#!/bin/bash

set -x

# export DISPLAY=:1.5
#Xvfb :1 -screen 5 5920x2080x8 &

# chromium

echo "About to set temp"
sudo sh -c 'echo 55000 > /sys/class/thermal/thermal_zone0/trip_point_4_temp'
echo "About to execute server"
/usr/bin/python3 /home/mendel/autoturret/coralboard/detect_server.py 
