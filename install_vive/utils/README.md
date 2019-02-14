# Overview

* [ROS Kinetic](#ros-install)
* [Textured Sphere](#textured-sphere-install)
* [USB Cam](#usb-cam-install)
* [Vive Plugin for Rviz](#vive-plugin-install)

## This Document
The purpose of this document is to provide isntructions for the installation of individual components for the Real Time VR project. Each individual component is organized to be easily reproducable or replaceable should you decide you want a different tool. **Please keep in mind** each is mildly dependent on file paths. If your setup crashes due to null pointers or memory leaks, you most likely have file path errors.

All scripts (except ros-install.sh) expect a catkin workspace directory to already exist. The directory does not have to be set up with src/ and build/ directories. The scripts do **not** run ``` catkin_make ``` or ``` catkin build ```.

## Contents

```tree
install
    ├── config
    │    ├── dual-cam.launch
    │    ├── single-cam.launch
    │    ├── vive.launch
    │    └── vive_launch_config.rviz
    ├── ros-install.sh
    ├── textured-sphere-install.sh
    ├── usb-cam-install.sh
    └── vive-plugin-install.sh
```

# Individual Installation Procedures

## ROS Install
To install ROS kinetic and dependencies: python-rosinstall, python-rosinstall-generator, python-wstool, and build-essential.

```bash
$ bash ros-install.sh
```

## Textured Sphere Install
To install Textured Sphere, run

```bash
$ bash textured-sphere-install.sh <relative/pathto/catkin-ws>
```

## USB Cam Install
To install USB cam, run

```bash
$ bash usb-cam-install.sh <relative/pathto/catkin-ws>
```

## Vive Plugin Install
To install the Vive Display plugin and dependencies: libglu1-mesa-dev, freeglut3-dev, mesa-common-dev, libogre-1.9-dev, steam, and nvidia driver.

```bash
$ bash vive-plugin-install.sh <relative/pathto/catkin-ws>
```

Once steam is installed, register/login to your account. Plug the HTC Vive into your computer and steam will automatically prompt you to install steamVR.