#!/usr/bin/env bash
# Authors:	Kate Baumli & John Sigmon & Beathan Andersen
# Date:		November 4, 2018
# Purpose:	This script kills all launches used in single_node_launch.sh
#		 	via ros, rviz plugin, and steam vr

STEAM=$(ps -ef | awk '/steam/ {print $2}')
kill "$STEAM" 2> /dev/null

OPENCV=$(ps -ef | awk '/opencv/ {print $2}')
kill "$OPENCV" 2> /dev/null

ROSCORE=$(ps -ef | awk '/roscore/ {print $2}')
kill "$ROSCORE" 2> /dev/null

LAUNCHSCRIPT=$(ps -uf | awk '/node_launch.sh/ {print $2}')
kill -9 "$LAUNCHSCRIPT" 2> /dev/null

ROSLAUNCH=$(ps -uf | awk '/roslaunch/ {print $2}')
kill -9 "$ROSLAUNCH" 2> /dev/null

RVIZ=$(ps -ef | awk '/rviz/ {print $2}')
kill -9 "$RVIZ" 2> /dev/null

USB_CAM=$(ps -ef | awk '/usb/ {print $2}')
kill -9 "$USB_CAM" 2> /dev/null

# Reset network configuration (i.e. replace /etc/hosts, /etc/network/interfaces, 
# and /etc/hostname with the originals we made backups of in "base_launch.sh")
if [ -f utils/netconfig/backups/interfaces-oldest ]; then
    mv utils/netconfig/backups/interfaces-oldest /etc/network/interfaces
elif [ -f utils/netconfig/backups/interfaces ]; then
    mv utils/netconfig/backups/interfaces /etc/network/interfaces
else
    echo "WARNING: Can't find backup network config interfaces file to restore earlier configuration"
fi
if [ -f utils/netconfig/backups/hosts-oldest ]; then
    mv utils/netconfig/backups/hosts-oldest /etc/hosts
elif [ -f utils/netconfig/backups/hosts ]; then
    mv utils/netconfig/backups/hosts /etc/hosts
else
    echo "WARNING: Can't find backup network config hosts file to restore earlier configuration"
fi
if [ -f utils/netconfig/backups/hostname-oldest ]; then
    mv utils/netconfig/backups/hostname-oldest /etc/hostname
elif [ -f utils/netconfig/backups/hostname ]; then
    mv utils/netconfig/backups/hostname /etc/hostname
else
    echo "WARNING: Can't find backup network config hostname file to restore earlier configuration"
fi
