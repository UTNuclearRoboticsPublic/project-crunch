###############################################################
# Purpose:      Creates GUI for the system launcher to wrap the
#               configuration and launch scripts.
# Written by:   Kate Baumli
# Modified:     Wednesday February 20, 2019
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

#TODO: Run kill_launch.sh on exit
#TODO: Add "back"  buttons to each page
#TODO: Make pretty layout
#TODO: Implement backend (actually configuring stuff/calling launch script)

class GUIWindow(QMainWindow):

    def __init__(self):
        super(GUIWindow, self).__init__()
        # Setup central widget for the window
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_widget.setLayout(QVBoxLayout())
        #self.second_page()
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
                if child.layout():
                    self.clear_layout(child.layout())

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
    @ChangeLayout(size=(250,150),title='Launch System')
    def first_page(self):
        '''Create layout of the first page'''
        layout = QVBoxLayout()
        launcher_button = QPushButton('Launch System')
        launcher_button.clicked.connect(self.tutorial_page0)
        layout.addWidget(launcher_button)
        return layout
   
    @ChangeLayout(size=(460,160),title="Launch Configurations")
    def tutorial_page0(self):
        layout = QVBoxLayout()
        num_headset_label = QLabel("How many headsets?")
        
        # Create horizontal layout for the two buttons
        btn_hbox = QHBoxLayout()

        one_headset_button = QPushButton(icon=QIcon("one-headset.png"))
        one_headset_button.setFixedHeight(131)
        one_headset_button.setFixedWidth(224)
        one_headset_button.setIconSize(QSize(129,222))
        one_headset_button.clicked.connect(self.one_headset_config)
        btn_hbox.addWidget(one_headset_button)

        two_headset_button= QPushButton(icon=QIcon("two-headsets.png"))
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
        self.tutorial_page1()    
     
    def two_headset_config(self):
        #TODO: set config = 2 headset
        self.tutorial_page1()    
    
    @ChangeLayout(size=(400,400))
    def tutorial_page1(self):
        layout = QVBoxLayout()
        tutorial_text = QLabel("Step 1: Make sure Vive is plugged into base station computer (this computer) and turned on.")
        done_button = QPushButton('Done')
        done_button.clicked.connect(self.on_done1_button_click)
        layout.addWidget(tutorial_text)
        layout.addWidget(done_button)
        return layout

    def on_done1_button_click(self):
        vive_plugged_in = True # TODO: Implement actual check
        if vive_plugged_in:
            self.tutorial_page2()
        else: 
            print("Error: Vive is not detected") # TODO: Make this text appear on the GUI in Red

    @ChangeLayout()
    def tutorial_page2(self):
        layout = QVBoxLayout()
        tutorial_text = QLabel("Step 2: Make sure cameras are plugged into the robot computer and turned on.")
        done_button = QPushButton('Done')
        done_button.clicked.connect(self.on_done2_button_click)
        layout.addWidget(tutorial_text)
        layout.addWidget(done_button)
        return layout
    
    def on_done2_button_click(self):
        cams_plugged_in = True # TODO: Implement actual check
        if cams_plugged_in:
            self.choose_catkin_directory()
        else: 
            print("Error: Cameras are not detected") # TODO: Make this text appear on the GUI in Red

  #  @ChangeLayout()
  #  def tutorial_page3(self):
  #      layout = QVBoxLayout()
  #      selection_prompt = "Please select your catkin directory"
  #      layout.addWidget(QLabel(selection_prompt))
  #      self.choose_catkin_directory()
  #      return layout

    @ChangeLayout()
    def choose_catkin_directory(self):
        # Have the user select her desired catkin workspace
        layout = QVBoxLayout()
        double_check_prompt = "Use this catkin directory?"
        layout.addWidget(QLabel(double_check_prompt))
        
        dialog = QFileDialog()
        finder_layout = QVBoxLayout()
        finder_layout.addWidget(dialog)
        selection_prompt = "Please select your catkin directory"
        text = dialog.getExistingDirectory(QWidget(), selection_prompt)
        if text != "": #TODO: Error checking for a proper catkin dir
            self.catkin = str(text)
            layout.addWidget(QLabel(self.catkin))
            ok_button = QPushButton("Yes")
            ok_button.clicked.connect(self.launch_system)
            layout.addWidget(ok_button)
        return layout

    def launch_system(self):
        self.buffer_page()
        # TODO: Run base launch script locally with proper configs
        subprocess.call(["launch_scripts/base_launch.sh","--catkin",self.catkin])
        # TODO: Run the robo launch script remotely with proper configs (if any)
        # TODO: Launch RViz & hopefully embed it into window & display stats

    @ChangeLayout()
    def buffer_page(self):
        layout = QVBoxLayout()
        text = QLabel("Launching System...")
        done_button = QPushButton('Done')
        done_button.clicked.connect(self.on_done2_button_click)
        layout.addWidget(text)
        return layout
        

if __name__ == "__main__":
    app = QApplication([sys.argv])
    main_window = GUIWindow()
    app.exec_()
