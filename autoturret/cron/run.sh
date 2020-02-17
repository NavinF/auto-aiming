#!/bin/bash

sudo sh -c 'echo 55000 > /sys/class/thermal/thermal_zone0/trip_point_4_temp'
python3 ~/autoturret/detect_server.py
