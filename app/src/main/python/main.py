###############################################################
# Purpose:      Creates GUI for the system launcher to wrap the
#               configuration and launch scripts.
# Written by:   Kate Baumli
# Modified:     Monday March 4, 2019
###############################################################
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout,QHBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObjectCleanupHandler
from PyQt5.QtCore import QSize
import functools
import sys
import subprocess
import os
import re
from fbs_runtime.application_context import ApplicationContext
#TODO: Add "back"  buttons to each page
#TODO: Make layout pretty

class GUIWindow(QMainWindow):

    def __init__(self,one_headset_img,two_headset_img, robo_launch,
                    base_launch, kill_launch):
        super(GUIWindow, self).__init__()
        self.one_headset_img = one_headset_img
        self.two_headset_img = two_headset_img
        self.robo_launch = robo_launch
        self.base_launch = base_launch
        self.kill_launch = kill_launch
        # Setup central widget for the window
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_widget.setLayout(QVBoxLayout())
        self.headset_refs = []
        self.get_env_vars()
        self.first_page()

    def closeEvent(self, event):
        # Override main window's function called when the red X is clicked 
        print("You closed the app!")
        #subprocess.call([self.kill_launch])

    def get_env_vars(self):
        self.robo_catkin = os.environ.get("ROBO_CATKIN")
        self.base_catkin = os.environ.get("BASE_CATKIN")
        self.robo_hostname = os.environ.get("ROBO_HOSTNAME")
        self.robo_username = os.environ.get("ROBO_USERNAME")

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
        layout = QVBoxLayout()
        info = QLabel("Make sure cameras are plugged into robot computer and turned on!")
        ok_button = QPushButton("OK, Got It!")
        ok_button.clicked.connect(self.how_many_headsets)
        layout.addWidget(info)
        layout.addWidget(ok_button)
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
        #TODO: set config = 1 headset
        self.two_headsets = False
        self.plug_in_headset()
     
    def two_headset_config(self):
        #TODO: set config = 2 headset
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
                self.launch_page()
                self.launch_system_backend()
        else:
            self.plug_in_headset(error=True)

    def get_new_vive_port(self):
        # TODO: Have this function find the port where the vive was just plugged
        #in, return None if there wasn't one plugged in. If there are multiple
        # vives plugged in, return port of most recently plugged in vive
        return "dummy"

    @ChangeLayout()
    def launch_page(self):
        layout = QVBoxLayout()
        text = QLabel("Launching system...")
        layout.addWidget(text)
        return layout

    def launch_system_backend(self):
        #self.launch_robo()
        self.launch_base()
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
        hmd1, err = subprocess.Popen(["wmctrl","-l","|","grep","HMD1"],
                stdout=subprocess.PIPE).communicate()
        self.wid1 = hmd1.split()[0]
        subprocess.call(["wmctrl","-ir",self.wid1,
                "-e","0,{},{},2160,1200".format(self.coords[0][0],self.coords[0][1])])
        
        if self.two_headsets:
            hmd2, err = subprocess.Popen(["wmctrl","-l","|","grep","HMD2"],
                    stdout=subprocess.PIPE).communicate()
            self.wid2 = hmd2.split()[0]

            subprocess.call(["wmctrl","-ir",self.wid2,
                    "-e","0,{},{},2160,1200".format(self.coords[1][0],self.coords[1][1])])



    def launch_robo(self):
        robo_client = self.robo_username + "@" + self.robo_hostname
        ssh_robo_launch_cmd = "ssh {} source {}".format(robo_client,self.robo_launch)
        subprocess.call(ssh_robo_launch_cmd.split(" "))
    
    def launch_base(self):
        subprocess.call([self.base_launch,"--catkin",self.base_catkin])
    

class AppContext(ApplicationContext):
    def run(self):
        # Get resources from resources folder
        # one headset image
        one_headset_img = self.get_resource("one-headset.png")
        # two headset image
        two_headset_img = self.get_resource("two-headset.png")
        # robo_launch.sh
        robo_launch = self.get_resource("robo_launch.sh")
        # base_launch.sh
        base_launch = self.get_resource("base_launch.sh")
        # kill_launch.sh
        kill_launch = self.get_resource("kill_launch.sh")
        main_window = GUIWindow(one_headset_img,two_headset_img,robo_launch,
                    base_launch, kill_launch)
        return self.app.exec_()
        
if __name__ == "__main__":
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
    
