#!/usr/bin/env bash

#####################################################################
# Parse args
#####################################################################
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    # Needs y or n
    --is_base)
    IS_BASE="$2"
    shift # past argument
    shift # past value
    ;;
    --robot_ip)
    ROBOT_IP="$2"
    shift # past argument
    shift # past value
    ;;
    --base_ip)
    BASE_IP="$2"
    shift # past argument
    shift # past value
    ;;
    --robot_hostname)
    ROBOT_NAME="$2"
    shift # past argument
    shift # past value
    ;;
    --base_hostname)
    BASE_NAME="$2"
    shift # past argument
    shift # past value
    ;;
    -p|--password)
    PASSWORD="$2"
    shift # past argument
    shift # past value
    ;;
esac
done

####################################################################
# Set ROS environment variables and set up network files
####################################################################
echo "export ROS_MASTER_URI=http://$ROBOT_IP:11311" >> ~/.bashrc

# Append ROS_IP to bashrc depending on which computer you are
if [ "$IS_BASE" == "y" ];
then
    echo "export ROS_IP=$BASE_IP" >> ~/.bashrc
elif [ "$IS_BASE" == "n" ];
then
    echo "export ROS_IP=$ROBOT_IP" >> ~/.bashrc
else
    echo "Unknown runtime error."
    exit 1
fi

# Get sudo privileges with the password arg
# Use it to add IPs and hostnames to files
echo "$PASSWORD" | sudo -S touch /etc/hosts
{
  echo "127.0.0.1       localhost"
  echo "$BASE_IP        $BASE_NAME"
  echo "$ROBOT_IP        $ROBOT_NAME"
} | sudo tee -a /etc/hosts

sudo touch /etc/hostname
if [ "$IS_BASE" == "y" ];
then
    echo "$BASE_NAME" | sudo tee -a /etc/hostname
elif [ "$IS_BASE" == "n" ];
then
    echo "$ROBOT_NAME" | sudo tee -a /etc/hostname
else
    echo "Unknown runtime error."
    exit 1
fi

# This allows ROS to use port 11311 permanently.
# This command only needs to run on the robot computer.
# If this is a security issue move this funcitonality into robo_launch.sh.
# Use the following command:
# sudo iptables -I INPUT -p tcp --dport 11311 --syn -j ACCEPT
# The port will be closed after a computer restart.
if [ "$IS_BASE" == "n" ];
then
    sudo ufw allow 11311/tcp
fi
