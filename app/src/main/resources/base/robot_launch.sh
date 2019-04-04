#!/usr/bin/env bash
#####################################################################
# Purpose: Launch robot station part of the system including camera 
#          setup and publishing, and roscore master
# Authors: Kate Baumli, Daniel Diamont, Caleb Johnson
# Date:    01/28/2019
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
MYFILENAME="robo_launch.sh"
if [[ -z "$LOGFILE" ]];
then
    LOGFILE="log$(timestamp)$MYFILENAME.txt"
fi

# SPHERE_LAUNCH="vive.launch"
SINGLE_CAM_LAUNCH="single-cam.launch"
DUAL_CAM_LAUNCH="dual-cam.launch"

#####################################################################
# Camera parsing function  --- works for Kodaks only
#####################################################################
function find_cam_dev_name {
    # shellcheck disable=SC2044
    # shellcheck disable=SC2106
	for sysdevpath in $(find /sys/bus/usb/devices/usb*/ -name dev); do
		(
			syspath="${sysdevpath%/dev}"
			devname="$(udevadm info -q name -p "$syspath")"
			[[ "$devname" == "bus/"* ]] && continue
			eval "$(udevadm info -q property --export -p "$syspath")"
			[[ -z "$ID_SERIAL" ]] && continue
			if [[ "$devname" == "video"* ]]
				then
					if [[ "$ID_SERIAL" == *"KODAK"* ]]
						then
							echo "/dev/$devname"
					fi
			fi
		)
	done
}


#####################################################################
 # Source devel/setup.bash and start roscore
#####################################################################
# shellcheck disable=SC1090
source "$CATKIN"/devel/setup.bash
x-terminal-emulator -e roscore

#####################################################################
 # Configure and launch cameras
#####################################################################
CAMS=$(find_cam_dev_name);
echo "[INFO: $MYFILENAME $LINENO] Cameras found at $CAMS" >> "$LOGFILE"
CAM_ARR=($CAMS)

# Get the video number of each camera
i=$((${#CAM_ARR[0]}-1))
CAM1=${CAM_ARR:$i:1}
i=$((${#CAM_ARR[1]}-1))
CAM2=${CAM_ARR[1]:$i:1}

if [[ ${#CAM_ARR[@]} == 1 ]];
then
    roslaunch --wait video_stream_opencv $SINGLE_CAM_LAUNCH video_stream_provider1:="$CAM1" &
    echo "[INFO: $MYFILENAME $LINENO] One camera launched from ${CAM_ARR[0]}" >> "$LOGFILE"
elif [[ ${#CAM_ARR[@]} == 2 ]];
then
    roslaunch --wait video_stream_opencv $DUAL_CAM_LAUNCH video_stream_provider1:="$CAM1" video_stream_provider2:="$CAM2" &
    echo "[INFO: $MYFILENAME $LINENO] Two cameras launched from ${CAM_ARR[0]} and ${CAM_ARR[1]}" >> "$LOGFILE"
else
    echo "[INFO: $MYFILENAME $LINENO] No cameras launched. Devices found at: $CAMS" >> "$LOGFILE"
fi

