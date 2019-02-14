#!/usr/bin/env bash
#
# Authors: John Sigmon and Daniel Diamont
# Last modified 11/18/18
#
# Purpose:
#	This script installs the ROS package usb_cam if it is not already installed

#####################################################################
# Parse args
#####################################################################
if [ $# -lt 2 ];
then
	echo "Usage: usb_cam_install.sh <-c|--catkin path to catkin workspace> [-l|--logfile logfile]"
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
MYFILENAME="usb_cam_install.sh"
if [[ -z "$LOGFILE" ]];
then
    LOGFILE="log$(timestamp)$MYFILENAME.txt"
fi

MYPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
BUILD="build"
SRC="src"
DEST="usb_cam"
LAUNCH="launch"
CONFIG="config"
SINGLECAM="single-cam.launch"
DUALCAM="dual-cam.launch"

#####################################################################
# Make Catkin dirs if not there and clone usb-cam
#####################################################################
if [ ! -d "$CATKIN"/"$BUILD" ];
then
	echo "[INFO: $MYFILENAME $LINENO] Making $BUILD dir in catkin workspace at $CATKIN" >> "$LOGFILE"
    mkdir -p "$CATKIN"/"$BUILD"
fi

if [ ! -d "$CATKIN"/"$SRC" ];
then
	echo "[INFO: $MYFILENAME $LINENO] Making $SRC dir in catkin workspace at $CATKIN" >> "$LOGFILE"
    mkdir -p "$CATKIN"/"$SRC"
fi

if [ ! -d "$CATKIN"/"$SRC"/"$DEST" ];
then
	echo "[INFO: $MYFILENAME $LINENO] Installing usb-cam into $CATKIN/$SRC/$DEST" >> "$LOGFILE"
    git clone https://github.com/ros-drivers/usb_cam.git "$CATKIN"/"$SRC"/"$DEST"/ &&
	echo "[INFO: $MYFILENAME $LINENO] Installed usb-cam into $CATKIN/$SRC/$DEST" >> "$LOGFILE"
fi

#####################################################################
# Copy launch files to usb_cam 'launch' dir
#####################################################################
if [ ! -f "$CATKIN"/"$SRC"/"$DEST"/"$LAUNCH"/"$SINGLECAM" ];
then
	echo "[INFO: $MYFILENAME $LINENO] Copying $SINGLECAM to $CATKIN/$SRC/$DEST/$LAUNCH/$SINGLECAM" >> "$LOGFILE"
    if ! cp "$MYPATH"/"$CONFIG"/"$SINGLECAM" "$CATKIN"/"$SRC"/"$DEST"/"$LAUNCH"/
    then
        echo "[ERROR: $MYFILENAME $LINENO] Copy $SINGLECAM to $CATKIN/$SRC/$DEST/$LAUNCH/$SINGLECAM failed." >> "$LOGFILE"
    fi
else
	echo "[INFO: $MYFILENAME $LINENO] $SINGLECAM already in $CATKIN/$SRC/$DEST/$LAUNCH/ , not copying." >> "$LOGFILE"
fi

if [ ! -f "$CATKIN"/"$SRC"/"$DEST"/"$LAUNCH"/"$DUALCAM" ];
then
	echo "[INFO: $MYFILENAME $LINENO] Copying $DUALCAM to $CATKIN/$SRC/$DEST/$LAUNCH/$DUALCAM" >> "$LOGFILE"
    if ! cp "$MYPATH"/"$CONFIG"/"$DUALCAM" "$CATKIN"/"$SRC"/"$DEST"/"$LAUNCH"/
    then
        echo "[ERROR: $MYFILENAME $LINENO] Copy $DUALCAM to $CATKIN/$SRC/$DEST/$LAUNCH/$DUALCAM failed." >> "$LOGFILE"
    fi
else
	echo "[INFO: $MYFILENAME $LINENO] $DUALCAM already in $CATKIN/$SRC/$DEST/$LAUNCH/ , not copying." >> "$LOGFILE"
fi
