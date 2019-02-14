#!/usr/bin/env bash
#
# Authors: John Sigmon and Daniel Diamont
# Last modified 11-18-18
# Purpose:
# This script installs the OSS plug-in for the Vive headset and SteamVR

#####################################################################
# Parse args
#####################################################################
if [ $# -lt 2 ];
then
	echo "Usage: vive_plugin_install.sh <-c|--catkin path to catkin workspace> [-l|--logfile logfile]"
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
MYFILENAME="vive_plugin_install.sh"
if [[ -z "$LOGFILE" ]];
then
    LOGFILE="log$(timestamp)$MYFILENAME.txt"
fi

#MYPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
BUILD="build"
SRC="src"
DEST="rviz_vive"
#CONFIG="config"
OGREFILES="/usr/include/OGRE/RenderSystems/GL/GL/."
OGREDEST1="/usr/include/OGRE/RenderSystems/GL/"
OGREDEST2="/usr/include/GL/"
#RVIZ_CONFIG_FILE="vive_launch_config.rviz"
#RVIZ_CONFIG="rviz_cfg"

mkdir -p "$CATKIN"/"$BUILD"
mkdir -p "$CATKIN"/"$SRC"

#####################################################################
# Install dependencies
#####################################################################
sudo apt-get update && sudo apt-get -y install freeglut3-dev=2.8.1-2\
                libglu1-mesa-dev=9.0.0-2.1\
                libogre-1.9-dev=1.9.0+dfsg1-7\
                mesa-common-dev=18.0.5-0ubuntu0~16.04.1

# shellcheck disable=SC2024
if ! sudo cp -a "$OGREFILES" "$OGREDEST1"
then
    echo "[ERROR: $MYFILENAME $LINENO] Copy $OGREFILES to $OGREDEST1 failed"
fi

# shellcheck disable=SC2024
if ! sudo cp -a "$OGREFILES" "$OGREDEST2"
then
    echo "[ERROR: $MYFILENAME $LINENO] Copy $OGREFILES to $OGREDEST1 failed"
fi

#####################################################################
# Install Steam
#####################################################################
if command -v steam > /dev/null
then
    echo "[INFO: $MYFILENAME $LINENO] Steam is already installed, skipping installation."
else
	sudo dpkg --add-architecture i386
    sudo apt-get update && sudo apt-get -y install gdebi-core\
                                    libgl1-mesa-dri:i386\
                                    libgl1-mesa-glx:i386\
                                    wget
    wget http://media.steampowered.com/client/installer/steam.deb
    yes | sudo gdebi steam.deb
    rm -f steam.deb*
    #sudo add-apt-repository multiverse
	#sudo apt update &> /dev/null
    #echo "[INFO: $MYFILENAME $LINENO] Installing Steam." >> "$LOGFILE"
	#sudo apt install steam
	#echo "[INFO: $MYFILENAME $LINENO] Steam is installed and being pushed to the background to update." >> "$LOGFILE"
	#bash steam &> /dev/null &
	#disown
fi

#####################################################################
# Install OpenVR
#####################################################################
if [ ! -d "$CATKIN"/"$SRC"/openvr ];
then
	echo "[INFO: $MYFILENAME $LINENO] Cloning OpenVR into $CATKIN/$SRC."
	git clone https://github.com/ValveSoftware/openvr.git "$CATKIN"/"$SRC"/openvr
fi

cd "$CATKIN"/"$SRC"/openvr || exit
if cmake .
then
    echo "[ERROR: $MYFILENAME $LINENO] Command 'cmake .' in $PWD failed." >> "$LOGFILE"
fi

if make
then
    echo "[ERROR: $MYFILENAME $LINENO] Command 'make' in $PWD failed." >> "$LOGFILE"
fi

cd - > /dev/null || exit

#####################################################################
# Install Vive Plug-in
#####################################################################
if [ ! -d "$CATKIN"/"$SRC"/"$DEST" ];
then
    echo "[INFO: $MYFILENAME $LINENO] Cloning $DEST in $CATKIN/$SRC."
    git clone https://github.com/btandersen383/rviz_vive "$CATKIN"/"$SRC"/"$DEST"/
    
    # If CATKIN is not absolute, make absolute for CMake file
    if [[ $CATKIN != '/'* ]];
    then
        CATKIN=$PWD/$CATKIN
    fi

    # Edit the CMakeList to point to OpenVR
    LINETOEDIT=30
    CMAKELISTS="$CATKIN"/"$SRC"/"$DEST"/CMakeLists.txt
    LINEBEFORE=$(head -"$LINETOEDIT" "$CMAKELISTS" | tail -1)
	sed -i "30s|.*|set(OPENVR \"${CATKIN}\/${SRC}\/openvr\")|" \
			"$CMAKELISTS"
    LINEAFTER=$(head -"$LINETOEDIT" "$CMAKELISTS" | tail -1)
    echo "[INFO: $MYFILENAME $LINENO] $CMAKELISTS for $DEST edited. Line $LINETOEDIT changed from $LINEBEFORE to $LINEAFTER"
else
	echo "[INFO: $MYFILENAME $LINENO] Vive plug-in is already cloned, skipping installation."
fi

# TODO
# Move config file to proper location
#cp $MYPATH/$CONFIG/$RVIZ_CONFIG_FILE $CATKIN/$SRC/$DEST/$RVIZ_CONFIG/$RVIZ_CONFIG_FILE

#####################################################################
# Install Nvidia Drivers
#####################################################################
DRIVER=$(sudo ubuntu-drivers devices | grep "recommended" | awk '{print $3}')
if dpkg -s "$DRIVER" &> /dev/null
then
    echo "[INFO: $MYFILENAME $LINENO] The recommended graphics drivers ($DRIVER) are already installed."
else
	echo "[INFO: $MYFILENAME $LINENO] Updating package lists with 'apt-get update'."
	#sudo add-apt-repository ppa:graphics-drivers/ppa
    #sudo apt update
	echo "[INFO: $MYFILENAME $LINENO] Installing $DRIVER"
	sudo apt-get -y install "$DRIVER"
fi
