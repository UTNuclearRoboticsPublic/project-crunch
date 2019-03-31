import os
import sys
from shutil import copyfile
import subprocess
from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                            QMessageBox, QInputDialog, QLineEdit, QFileDialog,
                           QDialogButtonBox, QMainWindow, QLabel)
from PyQt5.QtCore import QObjectCleanupHandler

class AppContext(ApplicationContext):
    """
    The AppContext holds the installer application. It serves to set up the
    main application, and wraps several bash scripts.

    The installer is a series of nested push-button functions, starting with
    first_page. The user is prompted for several bits of information, with 
    each information request leading to a new input dialog page. After all
    the information is collected, the exec_install function performs the core
    of the installation. Adding or modifying a step in the installation 
    process should occur within this exec_install function. If more information
    is required from the user, an input dialog function can be chained to the 
    end of the current chain.

    A similar chain of events happens for the ssh config button, prompting the
    user, then the core action happens inside #TODO function.
    """
    
    password = None
    install_dir = None
    catkin_dir = None
    current_computer_is_robot = None
    use_default_net_config = None

    robo_username = None
    robo_password = None
    robo_hostname = None
    
    def run(self):
        # Set up window
        self.window = QWidget()
        self.window.setLayout(self.first_page())
        self.window.resize(250,150)
        self.window.show()
        
        # Set default params
        self.ip_configs = {
            "robo_ip": "10.0.0.2",
            "base_ip": "10.0.0.1",
            "robo_hostname": "base",
            "base_hostname": "robo"
        }
        self.use_default_net_config = True
        return self.app.exec_()
    
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
        return layout

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
                'Please choose the directory where you wish to install Project\
                        Crunch.' 
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
                'Please choose the directory where you wish to create your\
                        catkin workspace.', 
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

    def install_finished(self):
        """
        Lets the user know that they are finished with the install.

        """
        layout = QVBoxLayout()
        dialog = QInputDialog()
        layout.addWidget(dialog)
        item, ok = dialog.getItem(
                     QWidget(),
                     'Install Complete!',
                     'You have completed the install process! You can run ' +
                     'Project Crunch by navigating to {} and clicking on the ' +
                     'FIX ME icon.\n\n You must restart your computer and ' + #TODO
                     'configure SSH keys before the application is fully ' +
                     'functional.',
                     ['OK'],
        )
        if ok:
            self.first_page()
        return layout #TODO does this return to first page
    
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
        widget = QWidget()
        base_ip_dialog = QInputDialog()
        robot_ip_dialog = QInputDialog()
        base_hostname_dialog = QInputDialog()
        robot_hostname_dialog = QInputDialog()
        base_ip, ok_1 = base_ip_dialog.getText(
                widget,
                '',
                'Enter the desired IP for the base station.\n\
                        Leave this field blank to use the defaults.', 
                QLineEdit.Normal, 
                '' 
        )#TODO this structure works just finish writing it 
        if ok_1:
            robot_ip, ok_2 = robot_ip_dialog.getText(
                    widget,
                    '',
                    'Enter the desired IP for the robot station.\n\
                            Leave this field blank to use the defaults.', 
                    QLineEdit.Normal, 
                    '' 
            )
        else:
            self.password = None
            self.first_page()
    
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

        # Export environment variables no matter what machine we are on (robot
        # or base.) We collect the envs from the opposite machine when the
        # user runs ssh config. Envs are written to the bashrc. Ideally they
        # are pruned at some point, but for now they just add new ones. This 
        # is OK because the new var is written to the end of the bashrc and 
        # so the definition overwrites any previous one. We need to check the 
        # current computer because the catkin workspace could be different.
        path_to_bashrc = os.path.join(os.path.expanduser('~'), '.bashrc')
        if self.current_computer_is_robot is True:
            with open(path_to_bashrc, "a") as f:
                f.write("export ROBO_CATKIN={}".format(self.catkin_dir))
        else:        
            with open(path_to_bashrc, "a") as f:
                f.write("export BASE_CATKIN={}\n".format(self.catkin_dir))
        with open(path_to_bashrc, "a") as f:
            f.write(
                    "export ROBO_HOSTNAME={}\n"\
                    .format(self.ip_configs['robo_hostname'])
            )
            f.write(
                    "export PROJECT_CRUNCH_INSTALL_PATH={}\n"\
                    .format(self.install_dir)
            ) 

        # Set up catkin workspace and install dependencies.
        # Script also sets up local hardware configurations for
        # Vive and OpenHMD.
        # Bash arguments are passed in via a dictionary and must match the
        # command line arguments of the script.
        install_args = [
            '-c', '{}'.format(self.catkin_dir), 
            '-i', '{}'.format(self.install_dir), 
            '-p', '{}'.format(self.password),
            '--openhmdrules', '{}'.format(self.get_resource('50-openhmd.rules')),
            '--viveconf', '{}'.format(self.get_resource('50-Vive.conf'))
        ]
        subprocess.run(
                [
                    'bash', 
                    self.get_resource('install.sh'), 
                    *install_args
                ], 
                check=True
        )

        # Copy over necessary configuration files
        # Still need openhmd file ## TODO fix last launch file
        single_cam_launch = 'single-cam.launch'
        dual_cam_launch = 'dual-cam.launch'
        vive_launch = 'vive.launch'
        opencv_dir = 'video_stream_opencv'
        txtsphere_dir = 'rviz_textured_sphere'

        txtsphere_dest_dir = os.path.join(self.catkin_dir, 'src', txtsphere_dir, 'launch')
        opencv_dest_dir = os.path.join(self.catkin_dir, 'src', opencv_dir, 'launch')

        # Copy single cam launch
        file_dest = os.path.join(opencv_dest_dir, single_cam_launch)
        if not os.path.isfile(file_dest):
            copyfile(self.get_resource(single_cam_launch), file_dest) 
        
        # Copy dual cam launch
        file_dest = os.path.join(opencv_dest_dir, dual_cam_launch)
        if not os.path.isfile(file_dest):
            copyfile(self.get_resource(dual_cam_launch), file_dest)
        
        # Copy rviz launch file
        file_dest = os.path.join(txtsphere_dest_dir, vive_launch)
        if not os.path.isfile(file_dest):
            copyfile(self.get_resource(vive_launch), file_dest)

        # Set up network configurations via /etc/hostnames
        if self.current_computer_is_robot == True:
            isbase = "n"
        else:
            isbase = "y"

        ip_args = [
            '--isbase', isbase,
            '--roboip', self.ip_configs['robo_ip'], 
            '--baseip', self.ip_configs['base_ip'], 
            '--robohostname', self.ip_configs['robo_hostname'],
            '--basehostname', self.ip_configs['base_hostname'], 
            '-p', '{}'.format(self.password)
        ]
        subprocess.run(
                [
                    'bash', 
                    self.get_resource('configure_network.sh'), 
                    *ip_args
                ], 
                check=True
        )
        
        # Set up main app

        # Set up icons?

        self.install_finished()

    def on_ssh_config_push(self):
        """
        This function begins execution of the SSH Key configuration chain of 
        events. The user is informed of assumptions, then is prompted for the
        robot username and password, as well as any custom hostname. The 
        configuration happens in the final step in exec_ssh_config().
        """
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(
                "The installation must have already been run on both the robot " +
                "and the base station.\n\nBoth computers should have been restarted." +
		"\n\nThe two computers must be connected " +
                "with a crossover ethernet cable, and you will need the username " +
                "and password for the robot, as well as any custom hostname it " +
                "may have been assigned."
        )
        msg.setWindowTitle("SSH key configuration")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
        #These are macros for the return values for StandardButtons
        #https://www.tutorialspoint.com/pyqt/pyqt_qmessagebox.htm
        CANCEL_BUTTON = 0x00400000
        OK_BUTTON =  0x00000400
        
        # If user cancels we return, if they choose OK we ask for information and then
        # execute the configuration.
        retval = msg.exec_()
        if retval == CANCEL_BUTTON:
            return
        elif retval == OK_BUTTON:
            self.get_robo_username()
   
    def get_robo_username(self):
        """
        Prompt user for robot username.
        """
        dialog = QInputDialog()
        text, ok = dialog.getText(
                QWidget(),
                'SSH Key Configuration',
                'Please enter the username for the robot. This is the same'\
                + ' username that you log into Ubuntu with.',
                QLineEdit.Normal,
                ""
        )
        if ok:
            self.robo_username = str(text)
            self.get_robo_password()
        else:
            self.robo_username = None
            # TODO what should the Default be? Empty username will crash program
            self.first_page()
    
    def get_robo_password(self):
        """
        Prompt user for robot password.
        """
        dialog = QInputDialog()
        text, ok = dialog.getText(
                QWidget(),
                'SSH Key Configuration',
                'Please enter the password for the robot.',
                QLineEdit.Password,
                ""
        )
        if ok:
            self.robo_password = str(text)
            self.get_robo_hostname()
        else:
            self.robo_password = None
            self.first_page()

    def get_robo_hostname(self):
        """
        Prompt user for robot hostname for SSH key configuration. If there
        is none, the user should input an empty string.
        """
        dialog = QInputDialog()
        text, ok = dialog.getText(
                QWidget(),
                'SSH Key Configuration',
                'If you installed with custom IP configurations, enter the '\
                + 'robot hostname now. Otherwise leave this entry blank.',
                QLineEdit.Normal,
                ""
        )
        if ok:
            if str(text) == "":
                self.robo_hostname = self.ip_configs['robo_hostname']
            else:
                self.robo_hostname = str(text)
            self.exec_ssh_config()
        else:
            self.robo_hostname = None
            self.first_page()
    
    def exec_ssh_config(self):
        """
        This function takes the previously gathered information and executes
        a bash script to complete the actual configuration steps.
        """
        ssh_config_args = [
            '--password', '{}'.format(self.robo_password),
            '--username', '{}'.format(self.robo_username),
            '--hostname', '{}'.format(self.robo_hostname)
        ]
        subprocess.run(
                [
                    'bash', 
                    self.get_resource('configure_ssh_keys.sh'), 
                    *ssh_config_args
                ], 
                check=True
        )
        

if __name__ == "__main__":
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
