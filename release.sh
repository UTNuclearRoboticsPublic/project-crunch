#!/usr/bin/bash

#TODO parse args and get v number

RELEASE_NAME=project-crunch-0.0.1

# Create build dir to hold our stuff
rm -rf build
mkdir -p build
mkdir -p build/Project-Crunch
mkdir -p build/Project-Crunch/Project-Crunch
mkdir -p build/Project-Crunch/Install

# Freeze both fbs projects
cd app
fbs freeze
cd ..
mv app/target/ build/Project-Crunch/Project-Crunch/target
cd build/Project-Crunch
cp Project-Crunch/target/Project-Crunch/Project-Crunch Project-Crunch/Project-Crunch.run
#ln -s Project-Crunch/target/Project-Crunch/Project-Crunch Project-Crunch/Project-Crunch
cd ../../

cd installer
fbs freeze
cd ..
mv installer/target/ build/Project-Crunch/Install/target
cd build/Project-Crunch
cp Install/target/Install/Install Install.run
#ln -s Install/target/Install/Install Install
cd ../../

# Create zip and tar
cd build
zip -r $RELEASE_NAME.zip Project-Crunch
tar -cvf $RELEASE_NAME.tar.gz Project-Crunch
