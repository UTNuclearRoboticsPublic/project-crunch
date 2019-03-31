#!/usr/bin/env bash

while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -a)
    ARG=$2
    shift
    shift
    ;;
esac
done

echo "hello world!"
echo "The next line should say arg!"
echo $ARG
