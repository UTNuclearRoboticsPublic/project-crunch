from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit, QFileDialog

import sys
import subprocess

# Get password input
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

def on_script_push():
    password = get_password()
    
    # Ask user for installation directory for app
    install_dir = get_install_dir()
    
    # Ask user for installation directory for catkin
    catkin_dir = get_catkin_dir()
    
    install_args = [
        '-c', '{}'.format(catkin_dir), 
        '-i', '{}'.format(install_dir), 
        '-p', '{}'.format(password)
    ]
    
    subprocess.run(['bash', 'install.sh', *install_args], check=True)
    # Run sudo prelim stuff
    # Run ros, other packages
    # Run post sudo stuff
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
    script_button = QPushButton('Run Test Script')
    script_button.clicked.connect(on_script_push)
    exit_button = QPushButton('Exit')
    exit_button.clicked.connect(on_exit_push)

    # Add buttons 
    layout.addWidget(script_button)
    layout.addWidget(exit_button)

    # Set layout
    window.setLayout(layout)
    window.show()
    app.exec_()
