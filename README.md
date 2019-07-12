# Project Crunch

## Introduction
This project is a virtual reality (VR) streaming system for the University of Texas at Austin [Nuclear Robotics Group](https://robotics.me.utexas.edu/) (UT NRG.)

This project allows operators to stream 360° video data from a remote computer to a local computer supporting one or two VR headsets in real time. This project is compatible with any two computers running Ubuntu 16.04, the HTC Vive headset, and two [Kodak SP360](https://kodakpixpro.com/cameras/360-vr/sp360-4k) cameras.

The necessary software can be installed via GitHub releases. The instructions can be found [here](#Downloading-and-Installation). If you would like to debug or maintain the software you can do so by cloning the repository. There are further instructions [here](#Modifying-and-Maintaining-the-Project).

This repository was initially designed and created by an ECE Senior Design team composed of: [Beathen Andersen](https://www.linkedin.com/in/beathan-andersen/), [Kate Baumli](https://www.linkedin.com/in/katebaumli/), [Daniel Diamont](https://www.linkedin.com/in/daniel-diamont/), [Bryce Fuller](https://www.linkedin.com/in/bryce-fuller/), [Caleb Johnson](https://www.linkedin.com/in/caleb-johnson-a96792149/), [John Sigmon](https://www.linkedin.com/in/john-sigmon/). The team was advised by [Dr. Mitchell Pyror](https://www.me.utexas.edu/faculty/faculty-directory/pryor), head of the University of Texas Nuclear Robotics Group.

---

## Table of Contents
1) [Download and Install](#Downloading-and-Installation) 
2) [Launch Project Crunch](#Launching-Project-Crunch) 
3) [Modify and Maintain the Project](#Modifying-and-Maintaining-the-Project) 
4) [Frequently Asked Questions](#FAQ)

---

## Downloading and Installation

This section details how to download the software and set it up for typical use. If you need to modify or debug the software, we recommend using the installation instructions [here](#Modifying-and-Maintaining-the-Project).

The provided installer must be run separately on the remote computer and the local computer (we will also refer to the remote computer as the base station.) After completing both installations and restarting the computers, they must be connected via ethernet and a local area network (LAN) must be set up. Once the network is set up, an additional installation step must be performed to configure [SSH](https://en.wikipedia.org/wiki/Secure_Shell) keys so that the two computers can communicate.
 
### System Requirements:

Ubuntu 16.04 is required on both computers. Other Ubuntu versions may work, but have not been tested. If you find that one works, please let us know! 

The installer will also install ROS Kinetic Desktop. 

Various other libraries are installed, to see all of them please check [this bash script](https://github.com/UTNuclearRoboticsPublic/project-crunch/blob/master/installer/src/main/resources/base/install.sh).

### Downloading from Release

1) Go to [Releases](https://github.com/UTNuclearRoboticsPublic/project-crunch/releases)
2) Download the `project-crunch-<version>.tar.gz` under assets
3) Extract the contents of the archive
4) Go to ```Project-Crunch``` and execute Install.run (Double click in finder, or ./Install.run from terminal)

### Download from Source

1) Set up a virtual environment, see [how to](#Setting-Up-a-Virtual-environment)
2) Download Latest Version with ```git clone https://github.com/UTNuclearRoboticsPublic/project-crunch.git```
3) Install requirements by first using cd to navigate to ```project-crunch``` then using  ```pip install -r requirements.txt```
4) Go to the ```installer``` directory and run ```fbs run```
5) Follow the [GUI installer](#navigating-the-installer-gui)

### Navigating the gui installer
1) Choose the Install Project Crunch option
2) Follow the on-screen prompts
3) Repeat steps 1-4 on the other computer
4) Choose SSH Key Configuration
5) Follow the on-screen prompts

--- 

## Setting-up Project Crunch
1) Connect the computers via ethernet
2) Plug the headset(s) into the local (base) computer
3) Connect the cameras to the remote computer and turn them on

## Running Project Crunch from Release from finder
4) On the local (base) computer, navigate to the directory where you installed Project Crunch. 
5) Open the `Project-Crunch` directory, and click `Project-Crunch.run`.
6) Follow the on-screen prompts.

## Running Project Crunch from Release from terminal
4) Run ```crunch``` in terminal
5) Follow the on-screen prompts

## Running Project Crunch from Source
4) On the local (base) computer, navigate to the directory where you installed project Crunch.
5) Run ```cd app/src/main/python```
6) Open main.py in the text editor of choice
7) Navigate to the comment on running from debug, comment the section above and uncomment it (As per the instructions there)
8) Run ```cd ../../../..```
9) Run ```setup_crunch```
10) run ```fbs run```
11) Follow the on-screen prompts
   
---

## Modifying and Maintaining the Project

TODO add explanation here

### Navigating the Repository

The installer lives under `installer/` and the main app lives under `app/`.

There is a minimal example with a working call to a bash script in `examples/src/`. Run it with `fbs run`.

### Setting Up a Virtual Environment

It is recommended to set up a virtual environment to contain the required python dependencies. Our prefered method is found below. 
Further reading on virtual environments in python can be found <a href="https://docs.python-guide.org/dev/virtualenvs/">here</a>, <a href="">here</a>, <a href="https://python-guide-cn.readthedocs.io/en/latest/dev/virtualenvs.html">here</a> and <a href="https://docs.python.org/3/tutorial/venv.html">here</a>.

From the top level of the repository (but inside of it), run:
```bash
$ virtualenv -p python3 .env
```

This sets up an entire python installation as an environment under the name `.env` which is not descriptive, but keeps you from having to remember how to activate all my different environments. 
Next activate the environment, and install all the python dependencies via the requirements file. 
When the environment is active it will display to the left of the prompt, as shown below (where the $ symbol indicates your prompt.)

```bash
$ source .env/bin/activate
(.env) $ pip install -r requirements.txt
```

When finished with the repository or environment, you can deactivate it with the simple command deactivate.

```bash
(.env) $ deactivate
$ 
```

### Pointing the App to a Repository Instead of a Release

If you wish to run the main app from the command line, you must first modify `app/src/main/python/main.py`. Go to the `get_env_vars()` function and find the code that assigns a path to `self.robot_launch` and `self.kill_launch`. There are alternate definitions for these variables commented out, they must be uncommented. TODO explain why

### Creating a New Release

There is a provided build script for generating a new release called `release.sh`. Before running check the following:

* Your local repository is on master by typing `git status`. 
* Your [virtual environment](#Setting-Up-a-Virtual-Environment) is activated.

The script will compile the projects and generate a tar file. All artifacts of the process are left in a `build/` directory. Running the script again automatically deletes the `build/` directory. You must follow the GitHub instructions to post the release to the repository. Be prepared to provide a short description of the changes and have a new version number ready. For more information on software versioning, please see [https://en.wikipedia.org/wiki/Software_versioning](https://en.wikipedia.org/wiki/Software_versioning).

### Release.sh Usage

The script must be run with the version number as an argument. For example:

```bash
bash release.sh --version 0.0.1
```

This generates the `build/` directory which contains a `.tar.gz`. Create a release by following the GitHub documentation [here](https://help.github.com/en/articles/creating-releases).

Future work? #TODO automate it https://developer.github.com/v3/guides/getting-started/
https://developer.github.com/v3/repos/releases/#create-a-release

---

## FAQ

> When I configure ssh keys, there is an error that says I only have one ssh key and I must manually reconfigure it. How do I do this?

* You typically generate an ssh key pair, which includes a private key and a public key. The installer was only able to find one of the keys. If you do not have any need for your current key setup or it is a mistake, you can simply delete the extra key and re-run the configuration. If your key was moved by mistake, you can move it back and re-run the configuration. The program looks for keys in the default location, which is `~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub`. If the program finds a key pair, it will just use the existing keys.

> When I install Nvidia drivers, the headset no longer works.

* If you are on a laptop, the Nvidia drivers have unknown issues with recognizing HMD devices as monitors. This is due (we think) to the built in desplay and its interaction with the graphics card. The configuration file we add that allows HMDs to be recognized on a given device does not seem to work when a built in display is being used. You can use the nouveau drivers with a single headset but this driver does not work for 2 headsets.

TODO create new sections for:
* TODO networking ports and firewall access how-to information
* TODO talk about choosing cameras for future use.
* TODO surround view information

---

