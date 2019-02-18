from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                            QMessageBox, QInputDialog, QLineEdit, QFileDialog,
                            QDialogButtonBox)

import os
import sys
from shutil import copyfile
import subprocess

def get_password():
    """Prompt user for password."""
    text, ok = QInputDialog.getText(
            QWidget(), 
            'Administrative Privileges Needed!', 
            'Please enter the password for the admin (root) user.', 
            QLineEdit.Password, 
            ""
    )
    if ok:
        return str(text)
    else:
        return None

def get_install_dir():
    """Prompt user for directory to install app."""
    text = QFileDialog.getExistingDirectory(
            QWidget(), 
            'Please choose the directory where you wish to install Project Crunch.' 
    )
    return str(text)

def get_catkin_dir():
    """Prompt user for catkin workspace."""
    text = QFileDialog.getExistingDirectory(
            QWidget(), 
            'Please choose the directory where you wish to create your catkin workspace.', 
    )
    return str(text)

def get_current_computer():
    """Prompt user for if they are running on robot or base station."""
    #text, ok = QInputDialog.getText(
    #        QWidget().resize(250,150), 
    #        'What computer are you installing on?',
    #        'Type in robot or base.', 
    #        QLineEdit.Normal, 
    #        ""
    #)
    #if ok:
    #    return str(text).lower()
    #else:
    #    return None
    
    
    
    #window = QWidget()
    #layout = QVBoxLayout()
    #isrobot = QDialogButtonBox(QDialogButtonBox.Yes |
    #        QDialogButtonBox.No)#QWidget())
    #window.setWindowTitle('Select computer')
    ##window.resize(250,150)

    #def return_robot():
    #    return "robot"

    #def return_base():
    #    return "base"

    #robot_button = QPushButton('Robot (Server)')
    #robot_button.clicked.connect(return_robot)
    #base_button = QPushButton('Base (Client)')
    #base_button.clicked.connect(return_base)
    
    #button_box.addButton(robot_button, QDialogButtonBox.AcceptRole)#, base_button
    #button_box.exec_()
    #layout.addWidget(button_box)
    #window.setLayout(layout)
    #window.show()

def get_ip_configs():
    """Prompt user for custom IP and hostnames."""
    # https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python

    # ask if they want to use custom ip, if not then return none
    # if yes, get them as strings and return a dictionary with the same form
    # as in on_install_push()
    pass #stub

# This is not used
def alert_popup():
    alert = QMessageBox()
    alert.setText('This button is useless!')
    alert.exec_()

def on_exit_push():
    """Exit when exit button pushed."""
    sys.exit()

def launch_file_config(catkin_dir):
    """Copy all necessary configuration files into app and catkin."""
    #TODO find location of these files
    #TODO probably remove unnecessary error handling (change to asserts?)
    single_cam_launch = 'single-cam.launch'
    dual_cam_launch = 'dual-cam.launch'
    vive_launch = 'vive.launch'
    path_to_single_cam_launch = ''
    path_to_dual_cam_launch = ''
    path_to_vive_launch = ''

    opencv_dir = 'video_stream_opencv'
    txtsphere_dir = 'rviz_textured_sphere'
    
    txtsphere_dest_dir = os.path.join(catkin_dir, 'src', opencv_dir, 'launch')
    opencv_dest_dir = os.path.join(catkin_dir, 'src', opencv_dir, 'launch')

    # Copy from resources to catkin
    if not os.path.isfile(path_to_single_cam_launch):
        file_dest = os.path.join(opencv_dest_dir, single_cam_launch)
        copyfile(path_to_single_cam_launch, file_dest) 
    if not os.path.isfile(path_to_dual_cam_launch):
        file_dest = os.path.join(opencv_dest_dir, dual_cam_launch)
        copyfile(path_to_dual_cam_launch, file_dest)
    if not os.path.isfile(path_to_vive_launch):
        file_dest = os.path.join(txtsphere_dest_dir, dual_cam_launch)
        copyfile(path_to_vive_launch, file_dest)

def on_install_push():
    """Install process on press of install button."""
#     password = get_password()
    
    #if password is None:
        # do something
    
    # Ask user for installation directory for app
#    install_dir = get_install_dir()
    
    # Ask user for installation directory for catkin
#    catkin_dir = get_catkin_dir()
   
    # Ask user which computre they are on
    computer = get_current_computer() #TODO make this a button
    
    # Ask user for custom IP configs
#    ip_configs = get_ip_configs()
    if ip_configs is None:
        ip_configs = {
            "robot_ip": "10.0.0.2",
            "base_ip": "10.0.0.1",
            "robot_hostname": "base",
            "base_hostname": "robot"
        }

    install_args = [
        '-c', '{}'.format(catkin_dir), 
        '-i', '{}'.format(install_dir), 
        '-p', '{}'.format(password)
    ]
    
    #subprocess.run(['bash', 'install_dependencies.sh', *install_args], check=True)

    # Copy over launch and config files
    launch_file_config(catkin_dir)

    if computer == "robot":
        isbase = "n"
    else:
        isbase = "y"

    install_args = [
        '--isbase', isbase,
        '--robotip', ip_configs['robot_ip'], 
        '--baseip', ip_configs['base_ip'], 
        '--robothostname', ip_configs['robot_hostname'],
        '--basehostname', ip_configs['base_hostname'], 
        '-p', '{}'.format(password)
    ]
    #TODO subprocess command not checked 
    #subprocess.run(['bash', 'configure_network.sh', *install_args], check=True)

    # Set up main app

    # Set up icons?

    # Remind user to restart and configure ssh keys

    print('end')

def on_ssh_config_push():
    # Running from base ?
    # Robot plugged in ?
    # Install ran on robot already ?
    
    # run bash script to setup keys
    # run bash script to test keys
    
    
    pass

if __name__ == "__main__":
    app = QApplication([sys.argv])
    window = QWidget()
    window.setWindowTitle('Installer')
    window.resize(250,150)
    layout = QVBoxLayout()


    # Make buttons
    install_button = QPushButton('Install Project Crunch')
    install_button.clicked.connect(on_install_push)
    ssh_config_button = QPushButton('Configure SSH Keys')
    ssh_config_button.clicked.connect(on_ssh_config_push)
    exit_button = QPushButton('Exit')
    exit_button.clicked.connect(on_exit_push)

    # Add buttons 
    layout.addWidget(install_button)
    layout.addWidget(ssh_config_button)
    layout.addWidget(exit_button)

    # Set layout
    window.setLayout(layout)
    window.show()
    app.exec_()
