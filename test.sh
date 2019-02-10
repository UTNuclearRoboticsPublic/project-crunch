#!/usr/env/bash bash

if [ $# -lt 2 ];
then
	echo "Usage: test.sh <-p|--password>"
	exit 1
fi

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -p|--password)
    PASSWORD=$2
    shift
    shift
    ;;
esac
done


echo $PASSWORD | sudo -S echo test
