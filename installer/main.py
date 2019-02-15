from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QFileDialog

import os
import sys
from shutil import copyfile
import subprocess

def get_password():
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
    text = QFileDialog.getExistingDirectory(
            QWidget(), 
            'Please choose the directory where you wish to install Project Crunch.' 
    )
    return str(text)

def get_catkin_dir():
    text = QFileDialog.getExistingDirectory(
            QWidget(), 
            'Please choose the directory where you wish to create your catkin workspace.', 
    )
    return str(text)

def alert_popup():
    alert = QMessageBox()
    alert.setText('This button is useless!')
    alert.exec_()

def on_exit_push():
    sys.exit()

def launch_file_config(catkin_dir):
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
        try:
            copyfile(path_to_single_cam_launch, file_dest) 
        except IOError:
            return None
    if not os.path.isfile(path_to_dual_cam_launch):
        file_dest = os.path.join(opencv_dest_dir, dual_cam_launch)
        try:
            copyfile(path_to_dual_cam_launch, file_dest)
        except IOError:
            return None
    if not os.path.isfile(path_to_vive_launch):
        file_dest = os.path.join(txtsphere_dest_dir, dual_cam_launch)
        try:
            copyfile(path_to_vive_launch, file_dest)
        except IOError:
            return None
   
    return True

def on_install_push():
    password = get_password()
    
    #if password is None:
        # do something
    
    # Ask user for installation directory for app
    install_dir = get_install_dir()
    
    # Ask user for installation directory for catkin
    catkin_dir = get_catkin_dir()
    
    install_args = [
        '-c', '{}'.format(catkin_dir), 
        '-i', '{}'.format(install_dir), 
        '-p', '{}'.format(password)
    ]
    
    #subprocess.run(['bash', 'install.sh', *install_args], check=True)

    # Copy over launch and config files
    if launch_file_config(catkin_dir) is None:
        print('error')#TODO refer to func declaration




    print('end')
    
    
    # Add app icon to Desktop?
    # Tell the user they completed installation
    # Collect all stdout, stderr into log?




if __name__ == "__main__":
    app = QApplication([sys.argv])
    window = QWidget()
    window.setWindowTitle('Installer')
    window.resize(250,150)
    layout = QVBoxLayout()


    # Make buttons
    install_button = QPushButton('Install Project Crunch')
    install_button.clicked.connect(on_install_push)
    exit_button = QPushButton('Exit')
    exit_button.clicked.connect(on_exit_push)

    # Add buttons 
    layout.addWidget(install_button)
    layout.addWidget(exit_button)

    # Set layout
    window.setLayout(layout)
    window.show()
    app.exec_()
