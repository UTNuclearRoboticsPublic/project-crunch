#!/usr/bin/env bash

#####################################################################
# Parse args
#####################################################################

MYFILENAME="install.sh"
 
if [ $# -lt 4 ];
then
    echo "[ERROR: $MYFILENAME $LINENO] Fewer than four arguments passed in."
    exit 1
fi

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -c|--catkin)
    CATKIN=$2
    shift
    shift
    ;;
    -i|--install)
    INSTALL=$2
    shift
    shift
    ;;
    -p|--password)
    PASSWORD=$2
    shift
    shift
    ;;
esac
done

BUILD="build"
SRC="src"
OPENCV_DEST="video_stream_opencv"
TXTSPHERE_DEST=""  #TODO
STEAMVR_DEST=""	   #TODO
LAUNCH="launch"
CONFIG="config"
SINGLECAM="single-cam.launch"
DUALCAM="dual-cam.launch"


#####################################################################
# Install dependencies
#####################################################################
echo "$PASSWORD" | sudo -S apt-get update && sudo apt-get -y install\
                        build-essential=12.1ubuntu2\
                        cmake=3.5.1-1ubuntu3\
                        git\
                        libgtest-dev=1.7.0-4ubuntu1\
                        v4l-utils=1.10.0-1 2>&1

#####################################################################
# Install ros-kinetic
#####################################################################
sudo apt-get update

if ! dpkg -s ros-kinetic-desktop-full > /dev/null
then
    echo "inside if statement 1"
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
    echo "[INFO: $MYFILENAME $LINENO] ros-kinetic-desktop-full already installed."

#####################################################################
# Install OpenCV Video streaming package
#####################################################################
mkdir -p "$CATKIN"/"$BUILD"
mkdir -p "$CATKIN"/"$SRC"

if [ ! -d "$CATKIN"/"$SRC"/"$OPENCV_DEST" ];
then
    echo "[INFO: $MYFILENAME $LINENO] Installing video_stream_opencv into $CATKIN/$SRC/$OPENCV_DEST"
    git clone https://github.com/ros-drivers/video_stream_opencv.git "$CATKIN"/"$SRC"/"$OPENCV_DEST"/ &&
    echo "[INFO: $MYFILENAME $LINENO] Installed video_stream_opencv into $CATKIN/$SRC/$OPENCV_DEST"
fi

echo "end of script"
