#!/usr/bin/env bash
#
# Written by John Sigmon and Bryce Fuller
# 
# This script does some of the heavy lifting for the install process,
# including installing the necessary system-wide dependencies and
# installing ROS if not installed. All of the necessary catkin work-
# space source code is installed here, although not all of the configuring
# is done inside this script.
# 
# For a complete stand-alone bash installation, please see:
# https://github.com/UTNuclearRoboticsPublic/ece-senior-design/tree/master/vive/install
# 
# The linked version above may become outdated and is considered deprecated and 
# is replaced with this installer.

#####################################################################
# Parse args
#####################################################################

MYFILENAME="install.sh"
 
if [ $# -lt 4 ];
then
    echo "[ERROR: $MYFILENAME $LINENO] Incorrect number of arguments passed in."
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
    --openhmdrules)
    OPENHMDRULES=$2
    shift
    shift
    ;;
    --viveconf)
    VIVECONF=$2
    shift
    shift
    ;;
esac
done

OPENCV_DEST="video_stream_opencv"
TXTSPHERE_DEST="rviz_textured_sphere"
OPENHMD_PLUGIN_DEST="rviz_openhmd"
OPENHMDRULES_DEST="/etc/udev/rules.d/"
VIVECONF_DEST="/usr/share/X11/xorg.conf.d/"
BUILD="build"
SRC="src"

mkdir -p "$CATKIN"/"$BUILD"
mkdir -p "$CATKIN"/"$SRC"

#####################################################################
# Install dependencies
#####################################################################
echo "$PASSWORD" | sudo -S apt-get update && sudo apt-get -y install\
                        build-essential=12.1ubuntu2\
                        cmake=3.5.1-1ubuntu3\
                        git\
                        libgtest-dev=1.7.0-4ubuntu1\
                        openssh-server\
			sshpass\
                        v4l-utils=1.10.0-1 2>&1

#####################################################################
# Install ros-melodic
#####################################################################
sudo apt-get update

if ! dpkg -s ros-melodic-desktop-full > /dev/null
then
    # Replaced $(lsb_release -sc) with xenial 
    # shellcheck disable=SC2016
    sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
    sudo apt-key adv \
        --keyserver 'hkp://keyserver.ubuntu.com:80' \
        --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
    sudo apt-get update && sudo apt-get -y install ros-melodic-desktop-full
    sudo rosdep init
    rosdep update
    echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
    # shellcheck disable=SC1090
    source ~/.bashrc
    echo "[INFO: $MYFILENAME $LINENO] Installed ros-melodic-desktop-full."
fi
    echo "[INFO: $MYFILENAME $LINENO] ros-melodic-desktop-full already installed."

#####################################################################
# Install OpenCV Video streaming package
#####################################################################
#TODO possibly checkout specific version of repo
if [ ! -d "$CATKIN"/"$SRC"/"$OPENCV_DEST" ];
then
    echo "[INFO: $MYFILENAME $LINENO] Installing video_stream_opencv into $CATKIN/$SRC/$OPENCV_DEST"
    git clone https://github.com/ros-drivers/video_stream_opencv.git "$CATKIN"/"$SRC"/"$OPENCV_DEST"/ &&
    echo "[INFO: $MYFILENAME $LINENO] Installed video_stream_opencv into $CATKIN/$SRC/$OPENCV_DEST"
fi

#####################################################################
# Install rviz textured sphere
#####################################################################
if [ ! -d "$CATKIN"/"$SRC"/"$TXTSPHERE_DEST" ];
then
	echo "[INFO: $MYFILENAME $LINENO] Cloning $TXTSPHERE_DEST into $CATKIN/$SRC."
    git clone https://github.com/UTNuclearRoboticsPublic/rviz_textured_sphere.git "$CATKIN"/"$SRC"/"$TXTSPHERE_DEST" &&
	echo "[INFO: $MYFILENAME $LINENO] $TXTSPHERE_DEST cloned to $CATKIN/$SRC/$TXTSPHERE_DEST"
else
    echo "[INFO: $MYFILENAME $LINENO] $TXTSPHERE_DEST is already cloned, skipping installation."
fi

#####################################################################
# Install OpenHMD plugin dependencies
#####################################################################
echo "$PASSWORD" | sudo -S apt-get update && sudo apt-get -y install\
                        libglu1-mesa-dev \
                        mesa-common-dev \
                        libogre-1.9-dev \
                        libudev-dev \
                        libusb-1.0-0-dev \
                        libfox-1.6-dev \
                        autotools-dev \
                        autoconf \
                        automake \
                        libtool \
                        libsdl2-dev \
                        libxmu-dev \
                        libxi-dev \
                        libgl-dev \
                        libglew1.5-dev \
                        libglew-dev \
                        libglewmx1.5-dev \
                        libglewmx-dev \
                        libhidapi-dev \
                        freeglut3-dev \
			wmctrl

# Install the OpenHMD plugin, this provides the OpenHMD dynamic library
if [ ! -d "$CATKIN"/"$SRC"/"$OPENHMD_PLUGIN_DEST" ];
then
	echo "[INFO: $MYFILENAME $LINENO] Cloning $OPENHMD_PLUGIN_DEST into $CATKIN/$SRC."
    git clone https://github.com/UTNuclearRoboticsPublic/rviz_openhmd.git "$CATKIN"/"$SRC"/"$OPENHMD_PLUGIN_DEST" &&
	echo "[INFO: $MYFILENAME $LINENO] $OPENHMD_PLUGIN_DEST cloned to $CATKIN/$SRC/$OPENHMD_PLUGIN_DEST"
else
    echo "[INFO: $MYFILENAME $LINENO] $OPENHMD_PLUGIN_DEST is already cloned, skipping installation."
fi

#####################################################################
# Vive and OpenHMD configuration
#####################################################################
# NVIDIA drivers
# Add apt-repo updates list of available drivers (which requires the user to hit enter)
# Checks for recommended drivers and installs them
echo | sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

# The following code searches for the recommended NVIDIA graphics driver and installs it.
# Use either this code block or nvidia-396 specified in the code block below this one.
#DRIVER=$(sudo ubuntu-drivers devices | grep "recommended" | awk '{print $3}')
#if dpkg -s "$DRIVER" &> /dev/null
#then
#    echo "[INFO: $MYFILENAME $LINENO] The recommended graphics drivers ($DRIVER) are already installed." 
#else
#    sudo apt-get -y install "$DRIVER" &&
#    echo "[INFO: $MYFILENAME $LINENO] $DRIVER installed."
#fi

# The following installs nvidia-396 driver. If recommended driver is preferred over
# nvidia-396, comment out this code block and uncomment the code block above this one.
if dpkg -s nvidia-396 &> /dev/null
then
    echo "[INFO: $MYFILENAME $LINENO] nvidia-396 graphics driver is already installed." 
else
    sudo apt-get -y install nvidia-396
    echo "[INFO: $MYFILENAME $LINENO] nvidia-396 installed."
fi

# Copy over rules files for using a HMD in Linux.
# This is required for Linux to allow access to a HMD.
# For more info: https://github.com/OpenHMD/OpenHMD/wiki/Udev-rules-list
if ! sudo cp "$OPENHMDRULES" "$OPENHMDRULES_DEST"
then
echo "[ERROR: $MYFILENAME $LINENO] Copy $OPENHMDRULES to $OPENHMDRULES_DEST failed"
    exit 1
fi

# Updates rules in OS for USB port access by OpenHMD plugin that come from the
# modified openHMD rules file above.
sudo udevadm control --reload-rules

# This config file tells the GPU to allow a HMD to be treated like a regular monitor.
# Without this, your GPU may block access to the HMD and make it appear as though
# it does not work.
# For more info: http://doc-ok.org/?p=1763
if ! sudo cp "$VIVECONF" "$VIVECONF_DEST"
then
    echo "[ERROR: $MYFILENAME $LINENO] Copy $VIVECONF to $VIVECONF_DEST failed"
    exit 1
fi

# Point resource file to openHMD resources directory.
# This config file points to the location of the compositor resources used in the plugin.
# It uses a hard coded absolute path to find the directory, so this needs to be set for each computer.
LINETOEDIT=3
FILETOEDIT="$CATKIN"/"$SRC"/"$OPENHMD_PLUGIN_DEST"/"$SRC"/resources.cfg
LINEBEFORE=$(head -"$LINETOEDIT" "$FILETOEDIT" | tail -1)
sed -i "${LINETOEDIT}s|.*|FileSystem=${CATKIN}/src/rviz_openhmd/src/resources/|" "$FILETOEDIT"
LINEAFTER=$(head -"$LINETOEDIT" "$FILETOEDIT" | tail -1)
echo "[INFO: $MYFILENAME $LINENO] $FILETOEDIT Line $LINETOEDIT changed from $LINEBEFORE to $LINEAFTER"

#Adds a ubuntu command to run crunch using a bash alias
echo "alias setup_crunch='source ~/.setup_crunch.sh'" >> ~/.bash_aliases
echo "alias crunch='setup_crunch && cd ~/Project-Crunch/Project-Crunch && ./Project-Crunch.run'" >> ~/.bash_aliases

# Run catkin_make to build ROS packages in catkin workspace
cd "$CATKIN"
catkin_make

# Change permissions on USB ports to all users.
# There is a potential security vulnerability opened by changing these permissions.
# It is required that the plugin have raw access to the USB port as only the plugin using OpenHMD,
# and not the OS (who usually intercepts data), knows how to handle the incomming information.
sudo chmod a+rw /dev/hidraw*

# We disable the firewall here. The reason is that we can predict port 22 (ssh) and 
# port 11311 (roscore), but the camera topics post to random ports and cannot be 
# predicted. There may be a method to pass in ports to the cameras via launch files,
# but this was not explored. The firewall is disabled by default, so we simply disable
# it. Check the documentation https://help.ubuntu.com/community/UFW for ufw to go back 
# to specifying specific ports.
sudo ufw disable
