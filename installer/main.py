from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                            QMessageBox, QInputDialog, QLineEdit, QFileDialog,
                           QDialogButtonBox, QMainWindow, QLabel)
from PyQt5.QtCore import QObjectCleanupHandler
import os
import sys
from shutil import copyfile
import subprocess
import functools

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
        self.ip_configs = {
            "robot_ip": "10.0.0.2",
            "base_ip": "10.0.0.1",
            "robot_hostname": "base",
            "base_hostname": "robot"
        }
    
    class ChangeLayout:
        """
        Decorator to wrap all page-defining functions to set the layout to the
        main widget; also updates size and window title if size is given to decorator
        (Simply replaces func with new_function)
        """
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
        """
        Create layout of the first page.
        """
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



    def on_install_push(self): 
        """
        Prompt user for password.
        """
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
        return layout 

    def install_directory(self):
        """
        Prompt user for directory to install app.
        
        Assigns the install directory to self as a full path.
        """
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
            self.catkin_directory()
        return layout

    def catkin_directory(self):
        """
        Prompt user for catkin workspace.

        Assigns the catkin directory to self as a full path.
        """
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
            self.select_comp()
        return layout

    def select_comp(self):
        """
        Prompt user for whether they are on robot or base computer.

        Assigns result to boolean class variable.
        """
        layout = QVBoxLayout()
        dialog = QInputDialog()
        layout.addWidget(dialog)
        item, ok = dialog.getItem(
                         QWidget(),
                         'Select Computer: Robot or Base',
                         "Are you currently installing on the robot computer?",
                         ['Yes','No'],
        )
        if ok:
            if str(item).lower() == "yes":
                self.current_computer_is_robot = True
            elif str(item).lower() == "no":
                self.current_computer_is_robot = False
            self.configure_ip()
        else:
            self.first_page()
        return layout

    def configure_ip(self):
        """
        Prompt user for whether they want custom IP and hostnames.

        If yes, next window is called and gets them. Else we execute
        the install process.
        """
        layout = QVBoxLayout()
        dialog = QInputDialog()
        layout.addWidget(dialog)
        item, ok = dialog.getItem(
                         QWidget(),
                         'Configuring IPs',
                         'Do you have custom IP configurations you would like to enter?',
                         ['Yes','No'],
        )
        if ok:
            if str(item).lower() == "yes":
                self.get_custom_ip_settings()
            elif str(item).lower() == "no":
                self.exec_install()
        else:
            self.first_page()
        return layout
    
    def get_custom_ip_settings(self):
         # https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python	
         # TODO Ask user for custom IP (y/n)
            # If yes, override defaults. Else return.
        """
        Prompt user for whether they want custom IP and hostnames.

        """
        #TODO make this take in four inputs
        widget = QWidget()
        layout = QVBoxLayout()
        base_ip_dialog = QInputDialog()
        robot_ip_dialog = QInputDialog()
        base_hostname_dialog = QInputDialog()
        robot_hostname_dialog = QInputDialog()
        layout.addWidget(
                base_ip_dialog,
#                robot_ip_dialog,
#                base_hostname_dialog,
#                robot_hostname_dialog,
        )
        text, ok = base_ip_dialog.getMultiLineText(
                widget, 
                '', 
                'Please enter the desired IP address for the base station.\n\
                        Leave this field blank to use the defaults.', 
                QLineEdit.Normal, 
                ""
        ) 
        if ok:

            self.first_page()
        else:
            self.password = None
            self.first_page()
        return layout 
    
    def exec_install(self):
        """
        Install process on press of install button.
        
        This executes the core functionality of the install process. In a
        nutshell, the steps are as follows:

          1. Export necessary environment variables to bashrc that are 
             needed for the main app.
          2. Run a bash script to set up a catkin workspace, install 
             dependencies via apt, and set up all the source code for the 
             catkin workspace.
          3. Copy over any necessary configuration and launch files into
             the catkin workspace.
          4. Run a bash script to set up the network configurations.

        """

        # Export environment variables to respective machines
        if self.current_computer_is_robot is True:
            with open("~/.bashrc", "a") as f:
                f.write("export ROBO_CATKIN={}".format(self.catkin_dir))
        else:        
            with open("~/.bashrc", "a") as f:
                f.write("export BASE_CATKIN={}".format(self.catkin_dir))
        
        # Export environment variables no matter what machine
        with open("~/.bashrc", "a") as f:
            f.write("export ROBO_HOSTNAME={}".format(self.ip_configs['robot_hostname']))
            f.write("export PROJECT_CRUNCH_INSTALL_PATH={}".format(self.install_dir)) 

        # Set up catkin workspace and install dependencies
        install_args = [
            '-c', '{}'.format(self.catkin_dir), 
            '-i', '{}'.format(self.install_dir), 
            '-p', '{}'.format(self.password)
        ]
        subprocess.run(['bash', self.get_resources('install_dependencies.sh'), *install_args], check=True)

        # Copy over necessary configuration files
        # Still need openhmd file ## TODO fix last launch file
        single_cam_launch = 'single-cam.launch'
        dual_cam_launch = 'dual-cam.launch'
        vive_launch = 'vive.launch'
        opencv_dir = 'video_stream_opencv'
        txtsphere_dir = 'rviz_textured_sphere'
        txtsphere_dest_dir = os.path.join(catkin_dir, 'src', opencv_dir, 'launch')
        opencv_dest_dir = os.path.join(catkin_dir, 'src', opencv_dir, 'launch')

        # Copy single cam launch
        file_dest = os.path.join(opencv_dest_dir, single_cam_launch)
        if not os.path.isfile(file_dest):
            copyfile(self.get_resource(single_cam_launch), file_dest) 
        
        # Copy dual cam launch
        file_dest = os.path.join(opencv_dest_dir, dual_cam_launch)
        if not os.path.isfile(file_dest):
            copyfile(self.get_resource(dual_cam_launch), file_dest)
        
        # Copy rviz launch file
        file_dest = os.path.join(txtsphere_dest_dir, dual_cam_launch)
        if not os.path.isfile(file_dest):
            copyfile(self.get_resource(vive_launch), file_dest)

        # Set up network configurations via /etc/hostnames
        if self.current_computer_is_robot == True:
            isbase = "n"
        else:
            isbase = "y"

        install_args = [
            '--isbase', isbase,
            '--robotip', self.ip_configs['robot_ip'], 
            '--baseip', self.ip_configs['base_ip'], 
            '--robothostname', self.ip_configs['robot_hostname'],
            '--basehostname', self.ip_configs['base_hostname'], 
            '-p', '{}'.format(password)
        ]
        subprocess.run(['bash', self.get_resource('configure_network.sh'), *install_args], check=True)
        
        # Reload rules, necessary for OpenHMD install
        subprocess.run(['udevadm', 'control', '--reload-rules'])
        
        
        # Set up main app

        # Set up icons?

        # Remind user to restart and configure ssh keys

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
