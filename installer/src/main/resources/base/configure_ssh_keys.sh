#!/usr/bin/env bash
#
# TODO

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -p)
    ROBO_PASSWORD=$2
    shift
    shift
    ;;
    -u)
    ROBO_USER=$2
    shift
    shift
    ;;
    -h)
    ROBO_HOSTNAME=$2
    shift
    shift
    ;;
esac
done

ssh-keygen -f ~/.ssh/id_rsa -t rsa -N '' || echo "keygen failed" && exit 1
sshpass -p "$ROBO_PASSWORD" ssh-copy-id "$ROBO_USER"@"$ROBO_HOSTNAME" || echo "sshpass copy ID failed" && exit 1 
ROBO_PASSWORD=""

ssh -i "$ROBO_USER"@"$ROBO_HOSTNAME" || echo "Unable to ssh into Robot after ssh key configuration" && exit 1

ROBO_CATKIN=$(ssh "$ROBO_USER"@"$ROBO_HOSTNAME" 'printf $ROBO_CATKIN')
echo "export ROBO_CATKIN=$ROBO_CATKIN" >> ~/.bashrc
echo "export ROBO_USER=$ROBO_USER" >> ~/.bashrc

# stash ssh command
# ssh root@remoteserver 'screen -S backup -d -m /root/backup.sh'
# from https://unix.stackexchange.com/questions/30400/execute-remote-commands-completely-detaching-from-the-ssh-connection
