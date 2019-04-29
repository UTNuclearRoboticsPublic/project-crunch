# Project Crunch

## Introduction
TODO give better project overview
The goal of this project is to build a long distance virtual reality (VR) streaming system for the University of Texas at Austin [Nuclear Robotics Group](https://robotics.me.utexas.edu/) (UT NRG.)

This software allows operators to control a robot which inspects radioactive nuclear facilities. It takes 360° video data, processes and formats it for compatibility with the HTC Vive headset, and transmits the VR stream to the headset. A remote computer is needed onboard the robot to process and transmit the camera stream.

The project is available via GitHub releases, and comes with an installer to configure your Linux environment, and a GUI to launch and configure cameras, ROS, RViz, and the Vive headset. The installer must be run on the base station computer and the remote computer aboard the robot. The installer also has an additional ssh configuration step that must be run on the base station with the remote computer attached via a local area network (LAN.)

This repository was initially designed and created by an ECE Senior Design team composed of: [Beathen Andersen](https://www.linkedin.com/in/beathan-andersen/), [Kate Baumli](https://www.linkedin.com/in/katebaumli/), [Daniel Diamont](https://www.linkedin.com/in/daniel-diamont/), [Bryce Fuller](https://www.linkedin.com/in/bryce-fuller/), [Caleb Johnson](https://www.linkedin.com/in/caleb-johnson-a96792149/), [John Sigmon](https://www.linkedin.com/in/john-sigmon/). The team was advised by Dr. Mitchell Pyror, head of the University of Texas Nuclear Robotics Group.

---

## Table of Contents
1) [Download and Install](#Downloading-and-Installation) 
    * [System Requirements](#System-Requirements) 
    * [Download Compiled Executable](#Download-Compiled-Executable) 
    * [Download Source](#Download-Source) 
        * [Set Up Environment](#Set-Up-Environment) 
        * [Download Latest Version (source)](#Download-Latest-Version-(source))       
        * [Build and Run Installer from Source](#Build-and-Run-Installer-from-Source)        
    * [Navigating the Installer GUI](#Navigating-the-Installer-GUI) 
    * [Configuring SSH Keys](#Configuring-SSH-Keys) 

2) [Launch Project Crunch](#Launching-Project-Crunch) 
    * [Launching Project Crunch from Executable](#Launching-Project-Crunch-from-Executable)   
    * [Launching Project Crunch from Source](#Launching-Project-Crunch-from-Source)    
    * [Navigating Project Crunch GUI](#Navigating-Project-Crunch-GUI) 

3) [Frequently Asked Questions](#FAQ)

4) [Modify and Maintain the Project](#Modifying-and-Maintaining-the-Project) 
    * [Navigating the Repository](#Navigating-the-Repository) 
    * [Setting Up a Virtual Environment](#Setting-Up-a-Virtual-Environment)   
    * [Pointing the App to a Repository Instead of a Release](#Pointing-the-App-to-a-Repository-Instead-of-a-Release) 
    * [Creating a New Release](#Creating-a-New-Release)   
    * [Release.sh Usage](#Release.sh-Usage) 
    
---

## Downloading and Installation
The two installation methods are: [Compiled Executable](#Download-Compiled-Executable) or [Compile from Source](#Download-Source). TODO mention why you would download one vs the other

### System Requirements:
Ubuntu 16.04 on both the base and remote computers. All other software dependancies are installed by our installer. TODO should we list what we install?

### Download Compiled Executable

1) Got to [Releases](https://github.com/UTNuclearRoboticsPublic/project-crunch/releases).
2) Download the `project-crunch-<version>.tar.gz` under assets 
3) Extract the contents and click on the Install.run icon. 
4) Follow the [GUI installer](#navigating-the-installer-gui) 

### Download Source

1) Set up a virtual environment, see [how to](#Setting-Up-a-Virtual-environment)
2) Install requirements with ```pip install -r requirements.txt```
3) Download Latest Version with ```git clone https://github.com/UTNuclearRoboticsPublic/project-crunch.git```
4) Go to the project directory and run ```fbs run```
5) Follow the [GUI installer](#navigating-the-installer-gui)

### Navigating the Installer GUI

TODO double check the steps are the same

1) Select /'Install Project Crunch/'
2) Enter the system administrator password
3) Specify whether you are installing on the robot computer, or the base station computer
4) Select the directory where you would like to install project-crunch
5) Click OK when you are given a warning about catkin workspaces
6) If you aren't sure about IP configs, select 'NO' when asked about custom IP configs
    
### Configuring SSH keys

TODO explain what this does
    
1) Launch Installer GUI
2) Select Configure SSH keys
3) If the RPS and LPS both have existing SSH configurations, enter them.
4) If you aren't sure about custom SSH configurations, a default configuration will be created for you. 
 
--- 

## Launching Project Crunch

### Launching from Release
TODO figure out where the launch executable is after installing from executable.
   
### Launching from Source
1) Navigate to project crunch directory and run ```fbs run``` 
2) Follow the [GUI prompts](#navigating-the-launcher-gui)

### Navigating the Launcher GUI
   Once the project-crunch GUI launches, follow the step-by step instructions
   -> Confirm the cameras and headsets are plugged in
   -> Select how many headsets will be used
   -> TODO: Cannot proceed further until I actually build and connect the LPS and RPS

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

## Modifying and Maintaining the Project
   * [Navigating the Repository](#Navigating-the-Repository) 
   * [Setting Up a Virtual Environment](#Setting-Up-a-Virtual-Environment)   
   * [Pointing the App to a Repository Instead of a Release](#Pointing-the-App-to-a-Repository-Instead-of-a-Release) 
   * [Creating a New Release](#Creating-a-New-Release)   
   * [Release.sh Usage](#Release.sh-Usage) 

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
(.env) $ pip install -r requirements
```

When finished with the repository or environment, you can deactivate it with the simple command deactivate.

```bash
(.env) $ deactivate
$ 
```

### Pointing the App to a Repository Instead of a Release

If you wish to run the main app from the command line, you must first modify `app/src/main/python/main.py`. Go to the `get_env_vars()` function and find the code that assigns a path to `self.robot_launch` and `self.kill_launch`. There are alternate definitions for these variables commented out, they must be uncommented.

### Creating a New Release

There is a provided build script for generating a new release called `release.sh`. Before running it make sure:

* Be sure your repository is on master by typing `git status`. 
* Be sure your [virtual environment](#Setting up a virtual environment) is activated.
* You have the Ubuntu `zip` utility installed. (`sudo apt-get install zip`)

The script will compile the projects and generate a tar file. All artifacts of the process are left in a `build/` directory. Running the script again automatically deletes the `build/` directory. You must follow the GitHub instructions to post the release to the repository. Be prepared to provide a short description of the changes and have a new version number ready. For more information on software versioning, please see [https://en.wikipedia.org/wiki/Software_versioning](https://en.wikipedia.org/wiki/Software_versioning).

### Release.sh Usage

The script must be run with the version number as an argument. For example:

```bash
bash release.sh --version 0.0.1
```

This generates the `build/` directory which contains a `.tar.gz`. Create a release by following the GitHub documentation [here](https://help.github.com/en/articles/creating-releases).

Future work? #TODO automate it https://developer.github.com/v3/guides/getting-started/
https://developer.github.com/v3/repos/releases/#create-a-release
