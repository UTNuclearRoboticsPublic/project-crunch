import os
import sys
from shutil import copyfile
import subprocess
from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                            QMessageBox, QInputDialog, QLineEdit, QFileDialog,
                           QDialogButtonBox, QMainWindow, QLabel)
from PyQt5.QtCore import QObjectCleanupHandler, QSize
from PyQt5.QtGui import (QIcon, QPixmap)

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
    user, then the core action happens inside exec_ssh_config function.
    """
    
    password = None
    install_dir = None
    catkin_dir = None
    current_computer_is_robot = None
    use_default_net_config = None
    robot_username = None
    robot_password = None
    robot_hostname = None
    
    def run(self):
        # Set up window
        self.window = QWidget()
        self.window.setLayout(self.first_page())
        self.window.resize(250,150)
        x , y = self.centerOnScreen()
        self.window.move(x,y)
        self.window.show()
        
        # Set default params
        self.ip_configs = {
            "robot_ip": "10.0.0.2",
            "base_ip": "10.0.0.1",
            "robot_hostname": "remote",
            "base_hostname": "base"
        }
        self.use_default_net_config = True
        return self.app.exec_()

    def centerOnScreen(self):
        '''
        centerOnScreen()
        Centers the window on the screen.
        '''
        resolution = QApplication.desktop().screenGeometry()
        x = (resolution.width() - self.window.width()) / 2
        y = (resolution.height() - self.window.height()) / 2
        return x , y

    def first_page(self):
        """
        Create layout of the first page.
        """
        layout = QVBoxLayout()
        instructions_button = QPushButton('Instructions')
        instructions_button.clicked.connect(self.on_instructions_push)
        install_button = QPushButton('Install Project Crunch')
        install_button.clicked.connect(self.on_install_push)
        ssh_config_button = QPushButton('Configure SSH Keys')
        ssh_config_button.clicked.connect(self.on_ssh_config_push)
        exit_button = QPushButton('Exit')
        exit_button.clicked.connect(self.on_exit_push)

        # Add buttons 
        layout.addWidget(instructions_button)
        layout.addWidget(install_button)
        layout.addWidget(ssh_config_button)
        layout.addWidget(exit_button)
        return layout

    def on_exit_push(self):
        sys.exit()
 
    def on_instructions_push(self):
        """
        Describe Project Crunch, function of Installer, LAN setup,
        Config SSH Keys, and the runtime app.
        """
        QMessageBox.about(self.window, 
                        "Instructions",
                        "Welcome to the Installer for Project Crunch!\n\n" +
                        "Project Crunch provides a graphical interface for " +
                        "improved situational awareness by interfacing " +
                        "virtual reality (VR) headsets with the Robotics " + 
                        "Operating System (ROS).\n\nThe role of this installer " +
                        "is to download and set up ROS, OpenHMD " +
                        "software to interface with the VR headsets, and other " +
                        "peripheral software. Perform installation of this " +
                        "software package by hitting 'OK' below, and clicking on " +
                        "'Install Project Crunch'.\n\n" +
                        "You will have to run the installation on both machines, then " +
                        "follow the instructions in " +
                        "'Configure SSH Keys' to complete the installation. " +
                        "The 'Configure SSH Keys' step should be run from the base station "+
                        "and with the remote computer hooked up via LAN. There is a walkthrough " +
                        "after clicking 'Configure SSH Keys'.\n\nAfter " +
                        "installation and SSH Key configuration " +
                        "is finished, " +
                        "Project Crunch can be executed via the Project-Crunch.run executable.")
        

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
            if self.is_password_correct():
                self.select_comp()
            else:
                self.password_incorrect()    
        else:
            self.password = None
            self.first_page()
        return layout 

    def is_password_correct(self):
        """
        This function tries the password assigned to self to run a test sudo 
        command. If the password is correct, the command makes a harmless echo
        and the function returns true. If incorrect, subprocess throws an 
        exception and we return false. Warning this has not been checked for
        security vulnerabilities.
        """
        try:
            out = subprocess.Popen(
                    ['echo', self.password], stdout=subprocess.PIPE)
            # check_output was returning output of 
            # dummy echo command, which was always 0.
            subprocess.check_output(
                    ['sudo','-S','whoami'], stdin=out.stdout) 
            out.wait()
        except subprocess.CalledProcessError:
            return False
        return True

    def password_incorrect(self):
        """
        This function tells the user they put in the wrong password and asks
        them to try again. It returns the user to the password input screen.
        """
        QMessageBox.about(self.window,
                    "Incorrect Password",
                    "The password entered was incorrect.\n" +
                    "Please try again.")
        self.on_install_push()

    def input_invalid(self):
        """
        This function tells the user that they gave the program invalid input asks
        them to try again. It returns and the calling function must return the user 
        to the screen they were already at.
        """
        msg = QMessageBox()
        msg.setInformativeText(
                    "You entered an invalid entry.\n" +
                    "Please try again."
        )
        msg.setWindowTitle("Invalid Input")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

        if retval == QMessageBox.Ok:
            return

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
                     "Are you on the robot computer?",
                     ['Yes','No'],
        )
        if ok:
            if str(item).lower() == "yes":
                self.current_computer_is_robot = True
            elif str(item).lower() == "no":
                self.current_computer_is_robot = False
            else:
                self.input_invalid()
                self.select_comp()
            self.install_directory()
        else:
            self.first_page()
        return layout
    

    def install_directory(self):
        """
        Prompt user for directory to install app.
        
        Assigns the install directory to self as a full path.
        """
        QMessageBox.about(self.window, 
                        "Installation Directory",
                        "Hit 'Ok', to chose a directory in which to install "+
                        "Project Crunch.")
 
        layout = QVBoxLayout()
        dialog = QFileDialog()
        layout.addWidget(dialog)
        text = dialog.getExistingDirectory(
                QWidget(), 
                'Choose directory to install Project Crunch.' 
        )
        if text == "":
            self.first_page() # Event triggered by hitting 'Cancel'
        else:    
            self.install_dir = str(text)
            self.install_info()
            #self.catkin_directory() # change to dialog box
        return layout

    def install_info(self):
        """
        This is a dialog box to warn the user. If you are on the robot, you are 
        prompted for the install directory, although we can't actually move the
        application to the install directory for you. We tell the user this, and
        let them know they will have to move the application to this directory
        at the end of the process. 
        """
        #TODO make note of this in the FAQ- moving into wrong dir could break the app
        layout = QVBoxLayout()
        reply = QMessageBox.question(QWidget(), 
                'Chosen Install Directory',
                'Once the install process has finished, ' +
                'you must copy the application over into ' +
                'its final destination, which you just chose. ' +
                'Be sure to write it down if needed, the install ' +
                'process can take up to twenty minutes on a ' +
                'clean machine.\n\nThe install directory you ' +
                'chose is:\n{}'.format(self.install_dir),
                QMessageBox.Ok, QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            self.catkin_directory()
        else:
            self.first_page()
        return layout

    def catkin_directory(self):
        """
        Prompt user for catkin workspace.

        Assigns the catkin directory to self as a full path.
        """
        if self.current_computer_is_robot:
            extra = "\n\n*Note:"\
            " Create catkin workspace in a different location " \
            "than project-crunch."
        else:
            extra = ""
        
        QMessageBox.about(self.window, 
                        "Catkin Workspace Directory",
                        "Hit 'Ok', to choose or create "+
                        "a catkin workspace, i.e., a directory in which to " +
                        "place all ROS packages and plugins for Project Crunch." +
                        "\n\n*Note:" +
                        "Create catkin workspace in a different location " +
                        "than project-crunch.")
        layout = QVBoxLayout()
        dialog = QFileDialog()
        layout.addWidget(dialog)
        text = QFileDialog.getExistingDirectory(
                QWidget(), 
                'Choose directory to create catkin workspace.', 
        )
        if text == "":
            self.first_page() # Event triggered by hitting 'Cancel'
        else:
            self.catkin_dir = str(text)
            self.catkin_info()
        return layout

    def catkin_info(self):
        """
        This function lets the user confirm the catkin directoryp that they selected.
        """
        layout = QVBoxLayout()
        reply = QMessageBox.question(QWidget(),
                     'Chosen Catkin Directory',
                     'The catkin directory you chose is:\n\n' +
                     self.catkin_dir +
                     '\nIf this is incorrect, please hit cancel to ' +
                     'select a different directory.',
                     QMessageBox.Ok, QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            self.configure_ip()
        else:
            self.catkin_directory()
        return layout
   
    def configure_ip(self):
        """
        Prompt user for whether they want custom IP and hostnames.

        If yes, next window is called and gets them. Else we execute
        the install process.
        """
        QMessageBox.about(self.window,
                "Custom IP Address Configuration",
                "The remote computer and the base computer each need to know " +
                "their Internet Protocol (IP) addresses in order to " +
                "communicate with each other across an Ethernet network.\n\n" +
                "The next screen will ask if you would like to use some default "+
                "IP addresses and hostnames that" +
                "we have assigned, or if you would like to input " +
                "your own.\n\n"+
                "[Hostname]\t[IP]"+
                "\n--------------------------------------------------"+
                "\nrobot\t\t10.0.0.2" +
                "\nbase\t\t10.0.0.1")

        layout = QVBoxLayout()
        dialog = QInputDialog()
        layout.addWidget(dialog)
        item, ok = dialog.getItem(
                     QWidget(),
                     'Configuring IPs',
                     'Use default IP configurations?',
                     ['Yes', 'No'],
        )
        if ok:
            if str(item).lower() == "no":
                self.get_custom_ip_settings()
            elif str(item).lower() == "yes":
                self.exec_install()
            else:
                self.invalid_input()
                self.configure_ip()
        else:
            self.first_page()
        return layout

    def get_custom_ip_settings(self):
        """
        Prompt user for whether they want custom IP and hostnames.

        """
        #TODO validate ip add
        # https://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python	
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
        )#TODO does this work?? 
        if ok_1:
            robot_ip, ok_2 = robot_ip_dialog.getText(
                    widget,
                    '',
                    'Enter the desired IP for the robot station.\n\
                            Leave this field blank to use the defaults.', 
                    QLineEdit.Normal, 
                    '' 
            )
            if ok_2:
                self.ip_configs['base_ip'] = base_ip
                self.ip_configs['robot_ip'] = robot_ip
                self.exec_install()
        else:
            self.password = None
            self.first_page()
    
    def exec_install(self):
        """
        Install process on press of install button.
        
        This executes the core functionality of the install process. In a
        nutshell, the steps are as follows:

          1. Export necessary environment variables to setup_crunch.sh that are 
             needed for the main app.
          2. Run a bash script to set up a catkin workspace, install 
             dependencies via apt, and set up all the source code for the 
             catkin workspace.
          3. Copy over any necessary configuration and launch files into
             the catkin workspace.
          4. Run a bash script to set up the network configurations.

        """
        
        # Tell the user not to worry about the program appearing to crash.
        # Note: this will halt the code here until the 'OK' button in the message box is clicked.
        # This will solve the problem for now but should have a better solution in the future.
        QMessageBox.about(self.window, 
                        "Installing",
                        "Installation and setup of the Robot Operating " +
                        "System, NVIDIA drivers, OpenHMD software, and " +
                        "peripheral software can take up to 20 min. " +
                        "The window may appear to stop responding, but " +
                        "we are installing in the background. Click 'OK' " +
                        "to begin the Installation and Setup.")

        # Export environment variables no matter what machine we are on (robot
        # or base.) We collect the envs from the opposite machine when the
        # user runs ssh config. Envs are written to setup_crunch.sh. Ideally they
        # are pruned at some point, but for now they just add new ones. This 
        # is OK because the new var is written to the end of the file
	# so the definition overwrites any previous one.
        # We need to check the current computer because the catkin workspace
        # could be different.
        path_to_setup_crunch = os.path.join(os.path.expanduser('~'), '.setup_crunch.sh')
        if self.current_computer_is_robot is True:
            with open(path_to_setup_crunch, "a") as f:
                f.write("export ROBOT_CATKIN_PATH={}\n".format(self.catkin_dir))
                f.write("export ROBOT_PROJECT_CRUNCH_PATH={}\n"\
                    .format(self.install_dir)) 
        else:        
            with open(path_to_setup_crunch, "a") as f:
                f.write("export BASE_CATKIN_PATH={}\n".format(self.catkin_dir))


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
        single_cam_launch = 'single-cam.launch'
        dual_cam_launch = 'dual-cam.launch'
        vive_launch = 'vive.launch'
        opencv_dir = 'video_stream_opencv'
        txtsphere_dir = 'rviz_textured_sphere'
        rviz_cfg = 'full_launch.rviz'
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
        
        # Copy rviz config file
        file_dest=os.path.join(self.catkin_dir,'src',txtsphere_dir,"rviz_cfg",rviz_cfg)
        if not os.path.isfile(file_dest):
            copyfile(self.get_resource(rviz_cfg),file_dest)

        # Set up network configurations via /etc/hostnames
        if self.current_computer_is_robot == True:
            is_base = "n"
        else:
            is_base = "y"

        ip_args = [
            '--is_base', is_base,
            '--robot_ip', self.ip_configs['robot_ip'], 
            '--base_ip', self.ip_configs['base_ip'], 
            '--robot_hostname', self.ip_configs['robot_hostname'],
            '--base_hostname', self.ip_configs['base_hostname'], 
            '--password', '{}'.format(self.password)
        ]
        subprocess.run(
                [
                    'bash', 
                    self.get_resource('configure_network.sh'), 
                    *ip_args
                ], 
                check=True
        )
        
        # TODO catkin build /make

        self.install_finished()

    def install_finished(self):
        """
        Lets the user know that they are finished with the install.

        """
        reply = QMessageBox.question(QWidget(),
                     'Install Complete!',
                     'You have completed the install process! ' +
                     'Copy the Project-Crunch directory to the ' +
                     self.install_dir +
                     ' directory you specified earlier. You can run ' +
                     'Project Crunch by navigating to the installation directory and clicking on the ' +
                     'Project-Crunch.run icon.\n\n You must restart your computer and ' + 
                     'configure SSH keys (in this order) before the ' +
                     'application is fully functional.' +
                     '\n\nWould you like us to restart now?',
                     QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                out = subprocess.Popen(
                        ['echo', self.password], stdout=subprocess.PIPE)
                subprocess.Popen(
                        ['sudo','-S','shutdown','-r', 'now'], stdin=out.stdout) 
                out.wait()
            except subprocess.CalledProcessError:
                self.error_during_restart()
        else:
            self.first_page()
   
    def error_during_restart(self):
        """
        Tells the user there was an error during restart.
        """
        QMessageBox.about(self.window,
                            "Error Restarting",
                            "There was an error restarting through the " +
                            "Installer. Please reboot computer manually.")
        self.first_page()
        pass

    def wrong_password(self):
        """
        Tells the user they input the wrong password and sends them back to the password screen.
        """
        QMessageBox.about(self.window,
                     "Incorrect Password",
                 "The password you entered was not correct.\n" +
                "Please try again.")
        self.on_install_push()
        pass

    def on_ssh_config_push(self):
        """
        This function begins execution of the SSH Key configuration chain of 
        events. The user is informed of assumptions, then is prompted for the
        robot username and password, as well as any custom hostname. The 
        configuration happens in the final step in exec_ssh_config().
        """
        msg = QMessageBox()
        msg.setInformativeText("To set up SSH keys, first setup a " +
                        "Local Area Network (LAN) " +
                        "between the two machines. Click 'Ok' to follow " +
                        "our tutorial to set-up the LAN and No to skip.")
        msg.setWindowTitle('LAN Walkthrough')
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel)
        msg.setFixedHeight(131)
        msg.setFixedWidth(224)
        
        retval = msg.exec_()

        if retval == QMessageBox.Ok:
           self.LAN_part_1()
        elif retval == QMessageBox.No:
           self.ssh_config_dialog()
        else:
           self.first_page()

    def LAN_part_1(self):
        msg = QMessageBox()
        #msg.setText("Crossover Cable")
        msg.setInformativeText("Make sure to connect both computers with " +
        "a cross-over Ethernet cable. An example of cross-over wiring is " +
        "shown on the left.")
        msg.setDetailedText("A straight-through cable is used to connect " +
                "routers to computers. In this case, to connect two computers " +
                "to each other, we need one computers TX wire to be the other's " +
                "RX wire, and vice versa. A crossover cable takes care of this. "
        )
        msg.setWindowTitle('Step 1) Crossover Cable')
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setFixedHeight(131)
        msg.setFixedWidth(224)
        pixmap = QPixmap(self.get_resource('crossover_cable.png'))
        pixmap.scaled(129, 222)
        msg.setIconPixmap(pixmap)
        
        retval = msg.exec_()

        if retval == QMessageBox.Ok:
            self.LAN_part_2()
        else:
            self.on_ssh_config_push()

    def LAN_part_2(self):
        msg = QMessageBox()
        #msg.setText("Connections Menu")
        msg.setInformativeText("Click on the Wi-Fi symbol on the " +
            "Ubuntu toolbar, and select 'Edit Connections'")
        msg.setWindowTitle('Step 2) Find the "Edit Connections" Menu')
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setFixedHeight(131)
        msg.setFixedWidth(224)
        pixmap = QPixmap(self.get_resource('wireless_menu.png'))
        pixmap.scaled(129, 222)
        msg.setIconPixmap(pixmap)
        
        retval = msg.exec_()

        if retval == QMessageBox.Ok:
            self.LAN_part_3()
        else:
            self.LAN_part_1()

    def LAN_part_3(self):
        msg = QMessageBox()
        #msg.setText("Connections Menu")
        msg.setInformativeText("Select 'Add'")
        msg.setWindowTitle('Step 3) Add Network Connection')
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setFixedHeight(131)
        msg.setFixedWidth(224)
        pixmap = QPixmap(self.get_resource('edit_connections_menu.png'))
        pixmap.scaled(129, 222)
        msg.setIconPixmap(pixmap)
        
        retval = msg.exec_()

        if retval == QMessageBox.Ok:
            self.LAN_part_4()
        else:
            self.LAN_part_2()
    
    def LAN_part_4(self):
        msg = QMessageBox()
        #msg.setText("Connections Menu")
        msg.setInformativeText("Choose 'Ethernet'")
        msg.setWindowTitle('Step 4) Choose Connection Type: Ethernet')
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setFixedHeight(131)
        msg.setFixedWidth(224)
        pixmap = QPixmap(self.get_resource('choose_connection_type.png'))
        pixmap.scaled(129, 222)
        msg.setIconPixmap(pixmap)
        
        retval = msg.exec_()

        if retval == QMessageBox.Ok:
            self.LAN_part_5()
        else:
            self.LAN_part_3()

    def LAN_part_5(self):
        msg = QMessageBox()
        #msg.setText("Connections Menu")
        msg.setInformativeText("Under the 'Ethernet' tab:\n\n" +
                "Edit the connection name, and choose " +
                "the 'Device' to be your machine's network card."
        )
        msg.setWindowTitle('Step 5) Choose Device (Network Card)')
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setFixedHeight(131)
        msg.setFixedWidth(224)
        pixmap = QPixmap(self.get_resource('choose_device.png'))
        pixmap.scaled(129, 222)
        msg.setIconPixmap(pixmap)
        
        retval = msg.exec_()

        if retval == QMessageBox.Ok:
            self.LAN_part_6()
        else:
            self.LAN_part_4()
    
    def LAN_part_6(self):
        msg = QMessageBox()
        #msg.setText("Connections Menu")
        msg.setInformativeText("Under the 'IPv4 Settings' tab:\n\n" +
                "Under 'Addresses' click 'Add' to enter the desired IP " +
                "address. The default for the base station is 10.0.0.1 and the default for the remote computer is 10.0.0.2. Network mask can be 255.255.255.0")
        msg.setWindowTitle("Step 6) Input IP Addresses")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setFixedHeight(131)
        msg.setFixedWidth(224)
        pixmap = QPixmap(self.get_resource('input_ip_addresses.png'))
        pixmap.scaled(129, 222)
        msg.setIconPixmap(pixmap)
        
        retval = msg.exec_()

        if retval == QMessageBox.Ok:
            self.LAN_part_7()
        else:
            self.LAN_part_5()
    
    def LAN_part_7(self):

        msg = QMessageBox()
        #msg.setText("Connections Menu")
        msg.setInformativeText("Make sure that steps 1-6 are complete " +
                "on both computers " +
                "before proceeding to the next step")
        msg.setWindowTitle("Step 7) Ensure steps 1-6 done on both computers")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setFixedHeight(131)
        msg.setFixedWidth(224)
        pixmap = QPixmap(self.get_resource('connection_established.png'))
        pixmap.scaled(129, 222)
        msg.setIconPixmap(pixmap)
        
        retval = msg.exec_()

        if retval == QMessageBox.Ok:
            self.LAN_part_8()
        else:
            self.LAN_part_6()
    
    def LAN_part_8(self):
        msg = QMessageBox()
        #msg.setText("Connections Menu")
        msg.setInformativeText("From each computer, right click the wireless connections " +
                "menu, and select the LAN you just created. You should see, " +
                "'Connection Established' as shown in the picture on the left.")
        msg.setWindowTitle("Step 8) Check for 'Connection Established'")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setFixedHeight(131)
        msg.setFixedWidth(224)
        pixmap = QPixmap(self.get_resource('connection_established.png'))
        pixmap.scaled(129, 222)
        msg.setIconPixmap(pixmap)
        
        retval = msg.exec_()

        if retval == QMessageBox.Ok:
            self.LAN_part_9()
        else:
            self.LAN_part_7()

    def LAN_part_9(self):
        msg = QMessageBox()
        #msg.setText("Connections Menu")
        msg.setInformativeText("To confirm that Ethernet cable is working properly, "+
                " open a terminal "+
                "and type 'ping <IP Address>', "+
                "where <IP Address is the IP of the other computer."+
                "\n\nIf ping test succeeds, then the LAN setup succeded"+
                " and you should see 0% packet loss like in the image " +
                "below.")
        msg.setWindowTitle("Step 8) Input IP Addresses")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.setFixedHeight(131)
        msg.setFixedWidth(224)
        pixmap = QPixmap(self.get_resource('ping_test.png'))
        pixmap.scaled(129, 222)
        msg.setIconPixmap(pixmap)
        
        retval = msg.exec_()

        if retval == QMessageBox.Ok:
            self.ssh_config_dialog()
        else:
            self.LAN_part_8()
    
    def ssh_config_dialog(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(
                "The installation must have already been run on both the robot " +
                "and the base station.\n\nBoth computers should have been restarted." +
		"\n\nThe two computers must be connected " +
                "with a crossover ethernet cable, and you will need the username " +
                "and password for the robot, as well as any custom hostname it " +
                "may have been assigned. This must be run from the base station."
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
            self.get_robot_username()

   
    def get_robot_username(self):
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
            self.robot_username = str(text)
            self.get_robot_password()
        else:
            self.robot_username = None
            # TODO what should the Default be? Empty username will crash program
            self.first_page()
    
    def get_robot_password(self):
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
            self.robot_password = str(text)
            self.get_robot_hostname()
        else:
            self.robot_password = None
            self.first_page()

    def get_robot_hostname(self):
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
                self.robot_hostname = self.ip_configs['robot_hostname']
            else:
                self.robot_hostname = str(text)
            self.exec_ssh_config()
        else:
            self.robot_hostname = None
            self.first_page()
    
    def exec_ssh_config(self):
        """
        This function takes the previously robot password, username, and 
        hostname and executes a bash script to complete the actual 
        configuration steps.
        """
        ssh_config_args = [
            '--password', '{}'.format(self.robot_password),
            '--username', '{}'.format(self.robot_username),
            '--hostname', '{}'.format(self.robot_hostname)
        ]
        subprocess.run(
                [
                    'bash', 
                    self.get_resource('configure_ssh_keys.sh'), 
                    *ssh_config_args
                ], 
                check=True
        )

        QMessageBox.about(
                self.window,
                "SSH Configuration Complete",
                "Both computers should be able to connect via SSH without entering a password."
        )
        

if __name__ == "__main__":
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
