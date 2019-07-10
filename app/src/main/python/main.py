##############################################################
# Purpose:      Creates GUI for the system launcher to wrap the
#               configuration and launch scripts.
# Written by:   Kate Baumli, Daniel Diamont, John Sigmon.
# Last Modified:     Saturday April 27, 2019
###############################################################
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObjectCleanupHandler
from PyQt5.QtCore import QSize
import functools
import sys
import subprocess
import signal
import os
import re
import time
from fbs_runtime.application_context import ApplicationContext
from traceback import print_exc

class GUIWindow(QMainWindow):

    def __init__(self,one_headset_img,two_headset_img, 
                    base_launch):
        super(GUIWindow, self).__init__()
        self.one_headset_img = one_headset_img
        self.two_headset_img = two_headset_img
        self.base_launch = base_launch
        # Setup central widget for the window
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_widget.setLayout(QVBoxLayout())
        self.headset_refs = []
        self.first_page()

    def closeEvent(self, event):
        # Override main window's function called when the red X is clicked 
        print("You closed the app!")
        robot_client = self.robot_username + "@" + self.robot_hostname
        sshProcess = subprocess.Popen(['ssh',
                                    robot_client],
                                    stdin=subprocess.PIPE,
                                    universal_newlines=True,
                                    bufsize=0,
                                    preexec_fn=os.setsid)
        sshProcess.stdin.write("pkill /opt/ros -f\n")        
        sshProcess.stdin.close()
        p = subprocess.Popen(['rosnode','kill','-a'])

    def get_env_vars(self):
        error_msg = ""
        missing_env_vars = 0
        self.robot_catkin = os.environ.get("ROBOT_CATKIN_PATH")
        self.base_catkin = os.environ.get("BASE_CATKIN_PATH")
        self.robot_hostname = os.environ.get("ROBOT_HOSTNAME")
        self.robot_username = os.environ.get("ROBOT_USERNAME")
        self.robot_project_crunch_path = os.environ.get("ROBOT_PROJECT_CRUNCH_PATH")

        if self.robot_catkin is None:
            error_msg += "ROBOT_CATKIN_PATH\n"
            missing_env_vars += 1
        if self.base_catkin is None: 
            error_msg += "BASE_CATKIN_PATH\n"
            missing_env_vars += 1
        if self.robot_hostname is None:
            error_msg += "ROBOT_HOSTNAME\n"
            missing_env_vars += 1
        if self.robot_username is None:
            error_msg += "ROBOT_USERNAME\n"
            missing_env_vars += 1
        if self.robot_project_crunch_path is None: 
            error_msg += "ROBOT_PROJECT_CRUNCH_PATH\n"
            missing_env_vars += 1
        if missing_env_vars > 0:
            if missing_env_vars == 1:
                return "The following environment variable is not properly set:\n\n"+error_msg+"\nPlease close the app, set it (either by rerunning\n the installer and ssh configuration or using\n'export {}=<value>') and try again.".format(error_msg.rstrip())
            else: 
                return "The following {} environment variables are not properly set:\n\n".format(missing_env_vars) + error_msg+"\nPlease close the app, set them (either by rerunning\n the installer and ssh configuration or using \n'export <ENVIRONMENT_VARIABLE_NAME>=<value>') and try again."
        else:
            # Use this section for running the launcher via
            # the zip or tar release, ie normal use.
            self.robot_launch = os.path.join(
                    self.robot_project_crunch_path,
                    "Project-Crunch",
                    "target", "Project-Crunch",
                    "robot_launch.sh"
            )
            # Use this section for running the launcher
            # in "debug" mode via fbs run, where the installation 
            # being considered is actually the repository.
            #self.robot_launch = os.path.join(
            #        self.robot_project_crunch_path, 
            #        "app", "src", 
            #        "main", "resources", "base",
            #        "robot_launch.sh"
            #)
            
            return None
    
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
                if child.layout():
                    self.clear_layout(child.layout())

        def __call__(inner_self,func):
            @functools.wraps(func) # Just keeps original function's special attributes
            def new_function(outer_self,**kwargs):
                if inner_self.size:
                    outer_self.resize(*inner_self.size)
                if inner_self.title:
                    outer_self.setWindowTitle(inner_self.title)
                # Delete the old layout
                inner_self.clear_layout(outer_self.main_widget.layout())
                QObjectCleanupHandler().add(outer_self.main_widget.layout())
                # Get and set the new layout
                if kwargs:
                    new_layout = func(outer_self,**kwargs)
                else:
                    new_layout = func(outer_self)
                outer_self.main_widget.setLayout(new_layout)
                outer_self.show()
            return new_function

    #######################################
    # Logic and page definitions start here
    #######################################
    @ChangeLayout(size=(250,150),title='Launch System')
    def first_page(self):
        '''Create layout of the first page'''
        layout = QVBoxLayout()
        launcher_button = QPushButton('Launch System')
        launcher_button.clicked.connect(self.info_page)
        layout.addWidget(launcher_button)
        return layout
   
    @ChangeLayout(size=(300,100))
    def info_page(self):
        error =  self.get_env_vars() # Either returns error msg or None
        if error is None:
            layout = QVBoxLayout()
            info = QLabel("Make sure cameras are plugged into robot computer and turned on!")
            ok_button = QPushButton("OK, Got It!")
            ok_button.clicked.connect(self.how_many_headsets)
            layout.addWidget(info)
            layout.addWidget(ok_button)
            return layout
        else:
            layout = QVBoxLayout()
            err_info = QLabel(error)
            layout.addWidget(err_info)
            return layout

    @ChangeLayout(size=(300,100),title="One or Two Headsets?")
    def how_many_headsets(self):
        layout = QVBoxLayout()
        num_headset_label = QLabel("How many headsets?")
        
        # Create horizontal layout for the two buttons
        btn_hbox = QHBoxLayout()

        one_headset_button = QPushButton(icon=QIcon(self.one_headset_img))
        one_headset_button.setFixedHeight(131)
        one_headset_button.setFixedWidth(224)
        one_headset_button.setIconSize(QSize(129,222))
        one_headset_button.clicked.connect(self.one_headset_config)
        btn_hbox.addWidget(one_headset_button)

        two_headset_button= QPushButton(icon=QIcon(self.two_headset_img))
        two_headset_button.setFixedHeight(131)
        two_headset_button.setFixedWidth(224)
        two_headset_button.setIconSize(QSize(129,222))
        two_headset_button.clicked.connect(self.two_headset_config)
        btn_hbox.addWidget(two_headset_button)
        
        layout.addWidget(num_headset_label)
        layout.addLayout(btn_hbox)
        return layout

    def one_headset_config(self):
        self.two_headsets = False
        self.plug_in_headset()
     
    def two_headset_config(self):
        self.two_headsets = True
        self.plug_in_headset(extra_str=" first ")    
    
    @ChangeLayout(size=(200,100),title="Prepare for System Launch")
    def plug_in_headset(self,extra_str=" ",error=False):
        layout = QVBoxLayout()
        if error: 
            label_str = "ERROR: headset not found. Please make sure Vive is turned on and try again."
        else: 
            label_str = "Plug in the"+extra_str+"headset, turn it on, and click \'Done\'"
        
        tutorial_text = QLabel(label_str)
        done_button = QPushButton('Done')
        done_button.clicked.connect(self.on_done_button_click)
        layout.addWidget(tutorial_text)
        layout.addWidget(done_button)
        return layout

    def on_done_button_click(self):
        new_vive_ref = self.get_new_vive_port()
        if new_vive_ref:
            self.headset_refs.append(new_vive_ref)
            if self.two_headsets and len(self.headset_refs) == 1:
                self.plug_in_headset(extra_str=" second ")
            else:
                self.runtime_page()
                self.launch_system_backend()
        else:
            self.plug_in_headset(error=True)

    def get_new_vive_port(self):
        # TODO: Have this function find the port where the vive was just plugged
        #in, return None if there wasn't one plugged in. If there are multiple
        # vives plugged in, return port of most recently plugged in vive
        return "dummy"

    @ChangeLayout(size=(200,200), title='Launching')
    def launch_page(self):
        layout = QVBoxLayout()
        text = QLabel("Launching System ...")
        layout.addWidget(text)
        return layout

    @ChangeLayout(size=(200,200), title="LAUNCHING SYSTEM...")
    def runtime_page(self):
        layout = QVBoxLayout()
        text = QLabel("System is Launched")
        layout.addWidget(text)

        #TODO figure out how to make the close button work, issue may be with imports
        kill = QPushButton('Kill System')
        kill.clicked.connect(self.closeEvent)
        layout.addWidget(kill)
        
        swap = QPushButton('Swap Windows')
        swap.clicked.connect(self.swap_windows)
        layout.addWidget(swap)

        return layout

    def launch_system_backend(self):
        self.launch_robot()
        self.launch_base()
        #ISSUE: temporary workaround to position windows running before OpenHMD plugin is added
        time.sleep(5)
        self.position_windows()

    def position_windows(self):
        p1 = subprocess.Popen(['xrandr'], stdout=subprocess.PIPE)
        opt, err = subprocess.Popen(['grep','2160x1200'],
                stdin=p1.stdout,
                stdout=subprocess.PIPE).communicate()
        list_of_opt = opt.splitlines()
        self.coords = []
        for line in list_of_opt:
            line = line.decode("utf-8", "ignore")
            try:
                res_coords = re.search("\d+x\d+\+\d+\+\d+",line).group()
                _ , x, y = res_coords.split("+")
                self.coords.append((x,y))
            except:
                pass
       
        # get HDMI/DP port ID using grep to find window position
        windows = subprocess.Popen(["wmctrl","-l"],stdout=subprocess.PIPE)
        hmd1, err = subprocess.Popen(['grep','HMD1'],
                        stdin=windows.stdout,
                                stdout=subprocess.PIPE).communicate()
        self.wid1 = hmd1.split()[0]
        #print(self.wid1)
        subprocess.call(["wmctrl","-ir",self.wid1,
            "-e","0,{},{},2160,1200".format(self.coords[0][0],self.coords[0][1])])

        if self.two_headsets:
            windows = subprocess.Popen(["wmctrl","-l"],stdout=subprocess.PIPE)
            hmd2, err = subprocess.Popen(["grep","HMD2"],
                        stdin=windows.stdout,
                        stdout=subprocess.PIPE).communicate()
            self.wid2 = hmd2.split()[0]
            subprocess.call(["wmctrl","-ir",self.wid2,
                "-e","0,{},{},2160,1200".format(self.coords[1][0],self.coords[1][1])])
        self.runtime_page()

    def swap_windows(self):
        if self.two_headsets:
            subprocess.call(["wmctrl","-ir",self.wid2,
                "-e","0,{},{},2160,1200".format(self.coords[0][0],self.coords[0][1])])
            subprocess.call(["wmctrl","-ir",self.wid1,
                "-e","0,{},{},2160,1200".format(self.coords[1][0],self.coords[1][1])])

    def launch_robot(self):
        try:
            robot_client = self.robot_username + "@" + self.robot_hostname
        except TypeError:
            # Prints the exception to stdout
            #TODO Is this exception still needed? Does it need to be hooked up to the env var error?
            print_exc()

        sshProcess = subprocess.Popen(['ssh',
                                    robot_client],
                                    stdin=subprocess.PIPE,
                                    universal_newlines=True,
                                    bufsize=0,
                                    preexec_fn=os.setsid)

        sshProcess.stdin.write("export DISPLAY=:0\n")
        sshProcess.stdin.write("source .bashrc\n")
        sshProcess.stdin.write("bash {} -c {}\n".format(self.robot_launch,
            self.robot_catkin))
        sshProcess.stdin.close()

        #sshProcess.kill()
        # send SIGTERM to all process groups so GUI does not hang.
        #os.killpg(os.getpgid(sshProcess.pid), signal.SIGTERM)
    
    def launch_base(self):
        my_env = os.environ.copy()
        my_env["PATH"] = "/usr/sbin:/sbin:" + my_env["PATH"]
        subprocess.Popen(
                [
                    "bash",
                    self.base_launch,
                    "--catkin",
                    self.base_catkin
                ],
                env=my_env
        )
    

class AppContext(ApplicationContext):
    def run(self):
        # Get resources from resources folder
        # one headset image
        one_headset_img = self.get_resource("one-headset.png")
        # two headset image
        two_headset_img = self.get_resource("two-headset.png")
        # base_launch.sh
        base_launch = self.get_resource("base_launch.sh")
        self.main_window = GUIWindow(one_headset_img,two_headset_img, base_launch)
        x , y = self.centerOnScreen()
        self.main_window.move(x,y)
        return self.app.exec_()

    def centerOnScreen(self):
        '''
        centerOnScreen()
        Centers the window on the screen.
        '''
        resolution = QApplication.desktop().screenGeometry()
        x = (resolution.width() - self.main_window.width()) / 2
        y = (resolution.height() - self.main_window.height()) / 2
        return x , y
        
if __name__ == "__main__":
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
    
