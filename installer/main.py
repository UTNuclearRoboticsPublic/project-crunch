from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                            QMessageBox, QInputDialog, QLineEdit, QFileDialog,
                           QDialogButtonBox, QMainWindow, QLabel)
from PyQt5.QtCore import QObjectCleanupHandler
import os
import sys
from shutil import copyfile
import subprocess
import functools

def get_ip_configs():

    # Ask user for custom IP configs
    ip_configs = get_ip_configs()
    if ip_configs is None:
        self.ip_configs = {
            "robot_ip": "10.0.0.2",
            "base_ip": "10.0.0.1",
            "robot_hostname": "base",
            "base_hostname": "robot"
        }
#    """Prompt user for custom IP and hostnames."""
    # https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python

    # ask if they want to use custom ip, if not then return none
    # if yes, get them as strings and return a dictionary with the same form
    # as in on_install_push()
#    pass #stub


def exec_install():
    """Install process on press of install button."""

    install_args = [
        '-c', '{}'.format(self.catkin_dir), 
        '-i', '{}'.format(self.install_dir), 
        '-p', '{}'.format(self.password)
    ]
    
    subprocess.run(['bash', 'install_dependencies.sh', *install_args], check=True)

    # Copy over launch and config files
    #launch_file_config(catkin_dir)

    if self.current_computer_is_robot == True:
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
    subprocess.run(['bash', 'configure_network.sh', *install_args], check=True)
    subprocess.run(['udevadm', 'control', '--reload-rules'])
    # Set up main app

    # Set up icons?

    # Remind user to restart and configure ssh keys

    #print('end')


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


class GUIWindow(QMainWindow):
    password = ""
    install_dir = ""
    catkin_dir = ""
    current_computer_is_robot = True
    use_default_net_config = True
    

    def __init__(self):
        super(GUIWindow, self).__init__()
        # Setup central widget for the window
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_widget.setLayout(QVBoxLayout())
        self.first_page()
    
    class ChangeLayout:
        ''' 
        Decorator to wrap all page-defining functions to set the layout to the
        main widget; also updates size and window title if size is given to decorator
        (Simply replaces func with new_function)
        '''
        def __init__(self, size=None, title=None):
            self.size = size
            self.title = title

        def clear_layout(self,layout):
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        def __call__(inner_self,func):
            @functools.wraps(func) # Just keeps original function's special attributes
            def new_function(outer_self):
                if inner_self.size:
                    outer_self.resize(*inner_self.size)
                if inner_self.title:
                    outer_self.setWindowTitle(inner_self.title)
                # Delete the old layout
                inner_self.clear_layout(outer_self.main_widget.layout())
                QObjectCleanupHandler().add(outer_self.main_widget.layout())
                # Get and set the new layout
                new_layout = func(outer_self)
                outer_self.main_widget.setLayout(new_layout)
                outer_self.show()
            return new_function

    #######################################
    # Logic and page definitions start here
    #######################################
    @ChangeLayout(size=(250,150),title='Installer')
    def first_page(self):
        '''Create layout of the first page'''
        layout = QVBoxLayout()
        install_button = QPushButton('Install Project Crunch')
        install_button.clicked.connect(self.on_install_push)
        ssh_config_button = QPushButton('Configure SSH Keys')
        ssh_config_button.clicked.connect(self.on_ssh_config_push)
        exit_button = QPushButton('Exit')
        exit_button.clicked.connect(self.on_exit_push)

        # Add buttons 
        layout.addWidget(install_button)
        layout.addWidget(ssh_config_button)
        layout.addWidget(exit_button)
        self.show()

        return layout
   
    @ChangeLayout()
    def on_exit_push(self):
        sys.exit()        


    def select_comp(self):
        '''Select whether the user is on robot or base computer.'''
        layout = QVBoxLayout()
        dialog = QInputDialog()
        layout.addWidget(dialog)
        item, ok = dialog.getItem(
                         QWidget(),
                         'Select Computer',
                         "Are you currently on the robot?",
                         ['yes','no'],
        )
        if ok:
            if str(item) == "yes":
                self.current_computer_is_robot = True
                #print("robot!")
            elif str(item) == "no":
                self.current_computer_is_robot = False
                #print("Base!")
        else:
            self.first_page()

        return layout

    def on_install_push(self): 
        """Prompt user for password."""
        layout = QVBoxLayout()
        dialog = QInputDialog()
        layout.addWidget(dialog)
        text, ok = dialog.getText(
                QWidget(), 
                'Administrative Privileges Needed!', 
                'Please enter the password for the admin (root) user.', 
                QLineEdit.Password, 
                ""
        ) 
        if ok:
            self.password = str(text)
            self.install_directory()
        else:
            self.password = None
            self.first_page()

        #print(self.password)
        return layout 

    def install_directory(self):
        """Prompt user for directory to install app."""
        layout = QVBoxLayout()
        dialog = QFileDialog()
        layout.addWidget(dialog)
        text = dialog.getExistingDirectory(
                QWidget(), 
                'Please choose the directory where you wish to install Project Crunch.' 
        )
        if text == "":
            self.first_page()
        else:    
            self.install_dir = str(text)
            #print(self.install_dir) 
            self.catkin_directory()

        return layout


    def catkin_directory(self):
        """Prompt user for catkin workspace."""
        layout = QVBoxLayout()
        dialog = QFileDialog()
        layout.addWidget(dialog)
        text = QFileDialog.getExistingDirectory(
                QWidget(), 
                'Please choose the directory where you wish to create your catkin workspace.', 
        )
        if text == "":
            self.first_page()
        else:
            self.catkin_dir = str(text)
            #print(self.catkin_dir)
            self.select_comp()

        return layout

    def on_ssh_config_push(self):
        # Running from base ?
        # Robot plugged in ?
        # Install ran on robot already ?
        
        # run bash script to setup keys
        # run bash script to test keys
    
        #TODO stub
        layout = QVBoxLayout()
        dialog = QInputDialog()
        layout.addWidget(dialog)
        item, ok = dialog.getItem(
                         QWidget(),
                         'Stub TODO',
                         "TODO",
                         ['todo'],
        )
        if ok:
            print("stub")

        return layout
 
   
if __name__ == "__main__":
    app = QApplication([sys.argv])
    main_window = GUIWindow()
    app.exec_()
