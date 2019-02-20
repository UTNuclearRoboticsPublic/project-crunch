#!/usr/bin/env bash
#####################################################################
# Purpose:       Launch base station part of the system including 
#                rviz, textured sphere, network, and VR plugin
# Authors:       Kate Baumli, Daniel Diamont, Caleb Johnson
# Last modified: 01/20/2019 by Kate
#####################################################################

function valid_ip()
{
    local  ip=$1
    local  stat=1

    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        OIFS=$IFS
        IFS='.'
        ip=($ip)
        IFS=$OIFS
        [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 \
            && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
        stat=$?
    fi
    return $stat
}


#####################################################################
# Parse args
#####################################################################

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

if [ -z "${CATKIN}" ];
then
    echo "ERROR: Must provide path to catkin workspace"
	echo "Usage: base_launch.sh <-c|--catkin path to catkin workspace> [-l|--logfile logfile] [-b basehostname] [-bip baseip] [-r robohostname] [-rip roboip]"
    exit 1
    # TODO: Make sure $CATKIN is a valid directory
fi

#####################################################################
# Configure log and vars
#####################################################################
timestamp() {
    date +"%T"
}
MYFILENAME="base_launch.sh"
if [[ -z "$LOGFILE" ]];
then
    LOGFILE="log$(timestamp)$MYFILENAME.txt"
fi

SPHERE_LAUNCH="vive.launch"
# RVIZ_CONFIG_FILE="rviz_textured_sphere.rviz"
# RVIZ_CONFIG="rviz_cfg"

#####################################################################
 # Source devel/setup.bash 
#####################################################################
# shellcheck disable=SC1090
source "$CATKIN"/devel/setup.bash

#####################################################################
 # Launch Rviz and textured sphere
#####################################################################
echo "[INFO: $MYFILENAME $LINENO] Attempting to launch rviz textured sphere with $SPHERE_LAUNCH" >> "$LOGFILE"
roslaunch --wait rviz_textured_sphere $SPHERE_LAUNCH && #configfile:="${RVIZ_CONFIG_FILE}"
echo "[INFO: $MYFILENAME $LINENO] rviz_textured_sphere launched with $SPHERE_LAUNCH" >> "$LOGFILE"
exit 0
