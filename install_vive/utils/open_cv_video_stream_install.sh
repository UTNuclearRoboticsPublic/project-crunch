#!/usr/bin/env bash
#
# Author: Kate Baumli 
# Modified: Beathan Andersen
# Last modified 12/11/18
#
# Purpose:
#	This script installs the ROS package video_stream_opencv if it is not already installed

#####################################################################
# Parse args
#####################################################################
if [ $# -lt 2 ];
then
	echo "Usage: open_cv_video_stream_install.sh <-c|--catkin path to catkin workspace> [-l|--logfile logfile]"
	exit 1
fi

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -c|--catkin)
    CATKIN=${2%/} # strip trailing slash
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
# Configure log and vars
#####################################################################
timestamp() {
    date +"%T"
}
MYFILENAME="open_cv_video_stream_install.sh"
if [[ -z "$LOGFILE" ]];
then
    LOGFILE="log$(timestamp)$MYFILENAME.txt"
fi

MYPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
BUILD="build"
SRC="src"
DEST="video_stream_opencv"
LAUNCH="launch"
CONFIG="config"
SINGLECAM="single-cam.launch"
DUALCAM="dual-cam.launch"

#####################################################################
# Make Catkin dirs if not there and clone video_stream_opencv
#####################################################################
mkdir -p "$CATKIN"/"$BUILD"
mkdir -p "$CATKIN"/"$SRC"

if [ ! -d "$CATKIN"/"$SRC"/"$DEST" ];
then
	echo "[INFO: $MYFILENAME $LINENO] Installing video_stream_opencv into $CATKIN/$SRC/$DEST"
    git clone https://github.com/ros-drivers/video_stream_opencv.git "$CATKIN"/"$SRC"/"$DEST"/ &&
	echo "[INFO: $MYFILENAME $LINENO] Installed video_stream_opencv into $CATKIN/$SRC/$DEST"
fi

#####################################################################
# Copy launch files to video_stream_opencv 'launch' dir
#####################################################################
if [ ! -f "$CATKIN"/$SRC/"$DEST"/"$LAUNCH"/"$SINGLECAM" ];
then
    echo "[INFO: $MYFILENAME $LINENO] Copying $SINGLECAM to $CATKIN/$SRC/$DEST/$LAUNCH/$SINGLECAM"
    if ! cp "$MYPATH"/"$CONFIG"/"$SINGLECAM" "$CATKIN"/"$SRC"/"$DEST"/"$LAUNCH"/
    then
        echo "[ERROR: $MYFILENAME $LINENO] Copy $SINGLECAM to $CATKIN/$SRC/$DEST/$LAUNCH/$SINGLECAM failed."
    fi
else
	echo "[INFO: $MYFILENAME $LINENO] $SINGLECAM already in $CATKIN/$SRC/$DEST/$LAUNCH/ , not copying."
fi

if [ ! -f "$CATKIN"/$SRC/"$DEST"/"$LAUNCH"/"$DUALCAM" ];
then
    echo "[INFO: $MYFILENAME $LINENO] Copying $DUALCAM to $CATKIN/$SRC/$DEST/$LAUNCH/$DUALCAM"
    if ! cp "$MYPATH"/"$CONFIG"/"$DUALCAM" "$CATKIN"/"$SRC"/"$DEST"/"$LAUNCH"/
    then
        echo "[ERROR: $MYFILENAME $LINENO] Copy $DUALCAM to $CATKIN/$SRC/$DEST/$LAUNCH/$DUALCAM failed."
    fi
else
	echo "[INFO: $MYFILENAME $LINENO] $DUALCAM already in $CATKIN/$SRC/$DEST/$LAUNCH/ , not copying."
fi
