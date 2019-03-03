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


# SSH KEY GENERATION
#
# Description:
#	We are creating RSA encryption public and private keys for the base
#	Then, the private key is added to the 'ssh-agent' service, which will
#	handle passwordless access in the future.
#	Lastly, we ssh into the remote machine to copy over the authorized key
#	from the base and set it with the approapriate access permissions. 
#
# Notes:
#	The following steps must occur sequentially.
#	Each command depends on the success of the last.
#
#	We use the program sshpass to pass in the remote password without having
#	a human type it in.
#
#	We use StrictHostKeyChecking=no to prevent the user having
#	to verify manually that we would like to connect to the remote.
#
#	We useIdentitiesOnly=yes to tell the host to only use the available
#	authentication identity file configured in ssh_config files, even if
#	ssh-agent offers more identities.
ssh-keygen -f ~/.ssh/id_rsa -t rsa -N "" \
 	&& ssh-add \
	&& cat ~/.ssh/id_rsa.pub | \
	sshpass -p "$ROBO_PASSWORD" \
	ssh -o StrictHostKeyChecking=no \
	 -o IdentitiesOnly=yes \
	 $ROBO_USER@$ROBO_HOSTNAME \
	 "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys"

ROBOT_PASSWORD=""

# Search through remote's .bashrc file for catkin workspace filepath.
# Note:
#	Vanilla ssh login only allows us to see a subset of the remote's
#	environment variables. Specifically, we can only see variables listed
#	under the remote's /.ssh/environment file. To bypass this problem,
#	we search through the remote's /.bashrc file for the 'export' command
#	associated with the environment variable of interest. We copy the
#	complete export command into our very own /bashrc file.
ROBO_CATKIN=$(ssh $ROBO_USER@$ROBO_HOSTNAME 'cat ~/.bashrc | grep ROBO_CATKIN')
echo "$ROBO_CATKIN" >> ~/.bashrc
echo "export ROBO_USER=$ROBO_USER" >> ~/.bashrc

# stash ssh command
# ssh root@remoteserver 'screen -S backup -d -m /root/backup.sh'
# from https://unix.stackexchange.com/questions/30400/execute-remote-commands-completely-detaching-from-the-ssh-connection

