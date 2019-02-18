from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObjectCleanupHandler
import functools
import sys

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

    @ChangeLayout(size=(250,150),title='Launch System')
    def first_page(self):
        '''Create layout of the first page'''
        layout = QVBoxLayout()
        launcher_button = QPushButton('Launch System')
        launcher_button.clicked.connect(self.on_launcher_button_click)
        advanced_button = QPushButton('Advanced Configurations...')
        advanced_button.clicked.connect(self.on_advanced_button_click)
        layout.addWidget(launcher_button)
        layout.addWidget(advanced_button)
        return layout
    
    @ChangeLayout(size=(400,400))
    def second_page(self):
        layout = QVBoxLayout()
        one_button = QPushButton('I am the only button on this page')
        layout.addWidget(one_button)
        return layout

    def on_launcher_button_click(self):
        print('Running on launcher button click')
        self.second_page()

    def on_advanced_button_click(self):
        print("Running on advanced button click")
    # def advanced_config_page(self):
        
   # def walk_through_setup(self):

   # def on_launch_button_push(self):
      #  walk_through_setup() 
     

if __name__ == "__main__":
    app = QApplication([sys.argv])
    main_window = GUIWindow()
    #main_window.show()
    app.exec_()
