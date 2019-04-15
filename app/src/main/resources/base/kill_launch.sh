#!/usr/bin/env bash
# Authors:	Kate Baumli & John Sigmon & Beathan Andersen
# Date:		November 4, 2018
# Purpose:	This script kills all launches used in single_node_launch.sh
#		 	via ros, rviz plugin, and steam vr

pkill -f /opt/ros
#STEAM=$(ps -ef | awk '/steam/ {print $2}')
#kill "$STEAM" 2> /dev/null

#rosnode kill --all

#OPENCV=$(ps -ef | awk '/opencv/ {print $2}')
#kill -9 "$OPENCV" 2> /dev/null

#LAUNCHSCRIPT=$(ps -uf | awk '/node_launch.sh/ {print $2}')
#kill -9 "$LAUNCHSCRIPT" 2> /dev/null

#ROSLAUNCH=$(ps -uf | awk '/roslaunch/ {print $2}')
#kill -9 "$ROSLAUNCH" 2> /dev/null

#RVIZ=$(ps -ef | awk '/rviz/ {print $2}')
#kill -9 "$RVIZ" 2> /dev/null

#USB_CAM=$(ps -ef | awk '/usb/ {print $2}')
#kill -9 "$USB_CAM" 2> /dev/null

#IMAGE_VIEW=$(ps -ef | awk '/image_view/ {print $2}')
#kill -9 "$IMAGE_VIEW" 2> /dev/null

#VIDEO_STREAM=$(ps -ef | awk '/video_stream_opencv/ {print $2}')
#kill -9 "$VIDEO_STREAM" 2> /dev/null

#ROSCORE=$(ps -ef | awk '/roscore/ {print $2}')
#kill -9 "$ROSCORE" 2> /dev/null
