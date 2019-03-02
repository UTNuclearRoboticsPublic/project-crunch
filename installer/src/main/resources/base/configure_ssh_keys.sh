#!/usr/bin/env bash
#
# TODO

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -p)
    ROBOT_PASSWORD=$2
    shift
    shift
    ;;
    -u)
    ROBOT_USER=$2
    shift
    shift
    ;;
    -h)
    ROBOT_HOSTNAME=$2
    shift
    shift
    ;;
esac
done

ssh-keygen -f ~/.ssh/id_rsa -t rsa -N '' || exit 1
sshpass -p "$ROBOT_PASSWORD" ssh-copy-id "$ROBOT_USER"@"$ROBOT_HOSTNAME" || exit 1 
ROBOT_PASSWORD=""

ssh -i "$ROBOT_USER"@"$ROBOT_HOSTNAME" || echo "Unable to ssh into Robot after ssh key configuration" && exit 1

printenv | grep "ROBO_CATKIN"   

# stash ssh command
# ssh root@remoteserver 'screen -S backup -d -m /root/backup.sh'
# from https://unix.stackexchange.com/questions/30400/execute-remote-commands-completely-detaching-from-the-ssh-connection
