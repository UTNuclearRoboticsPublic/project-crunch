#!/usr/bin/env bash
#
# Authors: Daniel Diamont and John Sigmon
#
# Purpose:
# 	This script installs the following packages if they are not already installed:
#		* ros-kinetic-desktop-full

#####################################################################
# Parse args
#####################################################################
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -h|--help)
    echo "Usage: ros_install.sh [-l|--logfile logfile]"
	exit 1
    shift # past argument
    shift # past value
    ;;
    -l|--logfile)
    LOGFILE="$2"
    shift # past argument
    shift # past value
    ;;
esac
done

#####################################################################
# Configure log
#####################################################################
timestamp() {
    date +"%T"
}

MYFILENAME="ros_install.sh"
if [[ -z "$LOGFILE" ]];
then
    LOGFILE="log_${MYFILENAME}_$(timestamp).txt"
fi

#####################################################################
# Install ROS-Kinetic and dependencies
#####################################################################
sudo apt-get update

if ! dpkg -s ros-kinetic-desktop-full > /dev/null
then
    # Replaced $(lsb_release -sc) with xenial 
    # shellcheck disable=SC2016
    sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu xenial main" > /etc/apt/sources.list.d/ros-latest.list'
    sudo apt-key adv \
        --keyserver hkp://ha.pool.sks-keyservers.net:80 \
        --recv-key 421C365BD9FF1F717815A3895523BAEEB01FA116
    sudo apt-get update && sudo apt-get -y install ros-kinetic-desktop-full
    sudo rosdep init
    rosdep update
    echo "source /opt/ros/kinetic/setup.bash" >> ~/.bashrc
    # shellcheck disable=SC1090
    source ~/.bashrc
    echo "[INFO: $MYFILENAME $LINENO] Installed ros-kinetic-desktop-full."
fi

sudo apt-get install -y ros-kinetic-camera-info-manager 2>&1 | tee -a "$LOGFILE" 
