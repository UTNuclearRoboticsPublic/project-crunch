# Project Crunch

---

## Introduction

The goal of this project is to build a long distance virtual reality (VR) streaming system for the University of Texas at Austin [Nuclear Robotics Group](https://robotics.me.utexas.edu/) (UT NRG.)

This software allows operators to control a robot which inspects radioactive nuclear facilities. It takes 360° video data, processes and formats it for compatibility with the HTC Vive headset, and transmits the VR stream to the headset. A remote computer is needed onboard the robot to process and transmit the camera stream.

The project is available via GitHub releases, and comes with an installer to configure your Linux environment, and a GUI to launch and configure cameras, ROS, RViz, and the Vive headset. The installer must be run on the base station computer and the remote computer aboard the robot. The installer also has an additional ssh configuration step that must be run on the base station with the remote computer attached via a local area network (LAN.)

This repository was initially designed and created by an ECE Senior Design team composed of: [Beathen Andersen](https://www.linkedin.com/in/beathan-andersen/), [Kate Baumli](https://www.linkedin.com/in/katebaumli/), [Daniel Diamont](https://www.linkedin.com/in/daniel-diamont/), [Bryce Fuller](https://www.linkedin.com/in/bryce-fuller/), [Caleb Johnson](https://www.linkedin.com/in/caleb-johnson-a96792149/), [John Sigmon](https://www.linkedin.com/in/john-sigmon/). The team was advised by Dr. Mitchell Pyror, head of the University of Texas Nuclear Robotics Group.

---

## Table of Contents
[Downloading and Installation](#Downloading-and-Installation)
[Launching project-crunch](#Launching-project/-crunch)
[FAQ](#FAQ)
[Modifying and Maintaining Project](#Modifying-and-Maintaining-Project)

---

## Downloading and Installation
    Table:
    System-Requirements
    Download-compiled-executable
    Download-source
    Navigating-the-installer-GUI
    Configuring SSH keys

### System Requirements:
Ubuntu 16.04 etc, Nvidia grpahics card

### Download compiled executable
   In the project-crunch github GUI, navigate to the Release tab.
   Download either the .zip or .tar.gz version of project-crunch-*** and expand the directory where you want project-crunch to reside. 
    
     > 'cd Project-Crunch'
     > './Install.run
   

-> Link to Navigating-the-Installer-GUI

### Download source
    Table:
    Set-up-environment
    Download Latest Version (source)
    Download Earlier Release (source)
    Build and run installer from source

#### Set up environment

   Download and install venv, FBS,  and other required packages
   Set up venv [->Link to venv section below]
   Then install fbs [-> Link to fbs installation page]
   
    
#### Download Latest Version (source)
    In a terminal, Navigate to the directory where the project-crunch folder will reside and enter. 
   > 'git clone https://github.com/UTNuclearRoboticsPublic/project-crunch.git' 
   
#### Download Earlier Release (source)
    In the project-crunch github GUI, navigate to the Release tab.
    Download either the Source_Code.zip, or Source_Code.tar.gz and expand the directory where you want project-crunch to reside. 
  
  
#### Build and run installer using fbs
    From the terminal, navigate into the Installer directory of project-crunch and enter:
    
   > 'cd project-crunch*/installer'
   
    Build and run the installer 
    
   > 'fbs run'

-> Link to Navigating-the-Installer-GUI
   

### Navigating the Installer GUI

    (bullet) Select /'Install Project Crunch/'
    (bullet) Enter the system administrator password
    (bullet) Specify whether you are installing on the robot computer, or the base station computer
    (bullet) Select the directory where you would like to install project-crunch
    (bullet) Click OK when you are given a warning about catkin workspaces
    (bullet) If you aren't sure about IP configs, select 'NO' when asked about custom IP configs
    
### Configuring SSH keys
    
    Launch Installer GUI
    Select Configure SSH keys
    If the RPS and LPS both have existing SSH configurations, enter them.
    If you aren't sure about custom SSH configurations, a default configuration will be created for you. 
 
## Launching project-crunch
    
    After project-crunch has been installed and SSH keys have been configured for the LPS and RPS, the system will be launched from the LPS.
    
    Table:
    Launching-project/-crunch-executable
    Launching-project/-crunch-from-source
    Navigating-project/-crunch-GUI

   ### Launching-project-crunch-executable
   TODO figure out where the launch executable is after installing from executable.
       
   ### Launching-project-crunch-from-source
   From the terminal, navigate into the project-crunch directory and enter:
    
   > 'cd project-crunch*/app'
   
    Build and run the Launcher 
    
   > 'fbs run'
   
   
   ### Navigating-project-crunch-GUI
       Once the project-crunch GUI launches, follow the step-by step instructions
       -> Confirm the cameras and headsets are plugged in
       -> Select how many headsets will be used
       -> TODO: Cannot proceed further until I actually build and connect the LPS and RPS



## FAQ

> When I configure ssh keys, there is an error that says I only have one ssh key and I must manually reconfigure it. How do I do this?

* You typically generate an ssh key pair, which includes a private key and a public key. The installer was only able to find one of the keys. If you do not have any need for your current key setup or it is a mistake, you can simply delete the extra key and re-run the configuration. If your key was moved by mistake, you can move it back and re-run the configuration. The program looks for keys in the default location, which is `~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub`. If the program finds a key pair, it will just use the existing keys.

### In Depth Troubleshooting

We recommend cloning the repository and running the project from the command line to debug more in depth errors. You may also reference the code documentation at #TODO. #TODO add more here as we come across it. Also include instructions for gathering stdout and stderr from the project. 

---

## Modifying and Maintaining the Project

---

### Navigating the Repository

The installer lives under `installer/` and the main app lives under `app/`.

There is a minimal example with a working call to a bash script in `examples/src/`. Run it with `fbs run`.

---

### Setting up a virtual environment

<p>
It is recommended to set up a virtual environment to contain the required python dependencies. (There are several ways to do this, the author's favorite is below)
Further reading on virtual environments in python can be found <a href="https://docs.python-guide.org/dev/virtualenvs/">here</a>, <a href="">here</a>, <a href="https://python-guide-cn.readthedocs.io/en/latest/dev/virtualenvs.html">here</a> and <a href="https://docs.python.org/3/tutorial/venv.html">here</a>.
</p>

From the top level of the repository (but inside of it), run:

```bash
virtualenv -p python3 .env
```

This sets up an entire python installation as an environment under the name `.env` which is not descriptive, but keeps you from having to remember how to activate all my different environments.

<p>
Next activate the environment, and install all the python dependencies via the requirements file. When the environment is active it will display to the left of the prompt, as shown below (where the $ symbol indicates your prompt.)
</p>

```bash
$ source .env/bin/activate
(.env) $ pip install -r requirements
```

<p>
When finished with the repository or environment, you can deactivate it with the simple command deactivate.
</p>

```bash
(.env) $ deactivate
$ 
```

---

### Pointing the app to a repository instead of a release

If you wish to run the main app from the command line, you must first modify `app/src/main/python/main.py`. Go to the `get_env_vars()` function and find the code that assigns a path to `self.robot_launch` and `self.kill_launch`. There are alternate definitions for these variables commented out, they must be uncommented.

---

### Creating a new release

There is a provided build script for generating a new release called `release.sh`. Before running it make sure:

* Be sure your repository is on master by typing `git status`. 
* Be sure your [virtual environment](#Setting up a virtual environment) is activated.
* You have the Ubuntu `zip` utility installed. (`sudo apt-get install zip`)

The script will compile the projects and generate a zip and a tar file. All artifacts of the process are left in a `build/` directory. Running the script again automatically deletes the `build/` directory. You must follow the GitHub instructions to post the release to the repository. Be prepared to provide a short description of the changes and have a new version number ready. For more information on software versioning, please see [https://en.wikipedia.org/wiki/Software_versioning](https://en.wikipedia.org/wiki/Software_versioning).

### Release.sh Usage

The script must be run with the version number as an argument. For example:

```bash
bash release.sh --version 0.0.1
```

This generates the `build/` directory which contains a `.tar.gz` and a `.zip`. Create a release by following the GitHub documentation [here](https://help.github.com/en/articles/creating-releases).

Future work? #TODO automate it https://developer.github.com/v3/guides/getting-started/
https://developer.github.com/v3/repos/releases/#create-a-release
