#!/usr/bin/env bash

#####################################################################
# Parse args
#####################################################################
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    # Needs y or n
    --isbase)
    ISBASE="$2"
    shift # past argument
    shift # past value
    ;;
    --roboip)
    ROBOIP="$2"
    shift # past argument
    shift # past value
    ;;
    --baseip)
    BASEIP="$2"
    shift # past argument
    shift # past value
    ;;
    --robohostname)
    ROBONAME="$2"
    shift # past argument
    shift # past value
    ;;
    --basehostname)
    BASENAME="$2"
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
echo "export ROS_MASTER_URI=http://$ROBOIP:11311" >> ~/.bashrc

# Append ROS_IP to bashrc depending on which computer you are
if [ "$ISBASE" == "y" ];
then
    echo "export ROS_IP=$BASEIP" >> ~/.bashrc
elif [ "$ISBASE" == "n" ];
then
    echo "export ROS_IP=$ROBOIP" >> ~/.bashrc
else
    echo "Unknown runtime error."
    exit 1
fi

# Get sudo privileges with the password arg
# Use it to add IPs and hostnames to files
echo "$PASSWORD" | sudo -S touch /etc/hosts
{
  echo "127.0.0.1       localhost"
  echo "$BASEIP        $BASENAME"
  echo "$ROBOIP        $ROBONAME"
} | sudo tee -a /etc/hosts

sudo touch /etc/hostname
if [ "$ISBASE" == "y" ];
then
    echo "$BASENAME" | sudo tee -a /etc/hostname
elif [ "$ISBASE" == "n" ];
then
    echo "$ROBONAME" | sudo tee -a /etc/hostname
else
    echo "Unknown runtime error."
    exit 1
fi
