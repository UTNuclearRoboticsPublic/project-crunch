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

ssh-keygen -f id_rsa -t rsa -N '' || exit 1
echo "$ROBOT_PASSWORD" > .tmp.txt
sshpass -f .tmp.txt ssh-copy-id "$ROBOT_USER"@"$ROBOT_HOSTNAME" || exit 1 

# stash ssh command
# ssh root@remoteserver 'screen -S backup -d -m /root/backup.sh'
# from https://unix.stackexchange.com/questions/30400/execute-remote-commands-completely-detaching-from-the-ssh-connection
