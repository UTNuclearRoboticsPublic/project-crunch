#!/usr/bin/env bash

# This script reads in a version number, creates a build directory
# and freezes both the launcher/app fbs project and the installer 
# fbs project. It links to the created executables and creates a 
# tar.

# Print usage
if [ $# -lt 2 ];
then
    echo "Usage:"
    echo "\tbash release.sh <-v|--version version number of release>"
    exit 1
fi

# Parse args
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
    -v|--version)
    VERSION="$2"
    shift # past argument
    shift # past value
    ;;
esac
done

RELEASE_NAME=project-crunch-$VERSION

# Create build dir to hold our stuff
rm -rf build
mkdir -p build
mkdir -p build/Project-Crunch
mkdir -p build/Project-Crunch/Project-Crunch
mkdir -p build/Project-Crunch/Install

# Freeze both fbs projects and create links to the executables
cd app
fbs freeze
cd ..
mv app/target/ build/Project-Crunch/Project-Crunch/target
cd build/Project-Crunch/Project-Crunch
ln -s target/Project-Crunch/Project-Crunch Project-Crunch.run
cd ../../../

cd installer
fbs freeze
cd ..
mv installer/target/ build/Project-Crunch/Install/target
cd build/Project-Crunch
ln -s Install/target/Install/Install Install.run
cd ../../

# Create tar in build folder
cd build
tar -cvf $RELEASE_NAME.tar.gz Project-Crunch
