from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QInputDialog, QLineEdit

import sys
import subprocess

# Get password input
def get_text():
    text, ok = QInputDialog.getText(QWidget(), 'Text Box', 'Test', QLineEdit.Normal, "")
    if ok:
        print(str(text))
    return str(text)

def on_extra_push():
    alert = QMessageBox()
    alert.setText('This button is useless!')
    alert.exec_()

def on_exit_push():
    sys.exit()

def on_test_script_push():
    password = get_text()
    subprocess.run(['bash', 'test.sh', '-p {}'.format(password)], check=True)

app = QApplication([sys.argv])
window = QWidget()
layout = QVBoxLayout()

# Make buttons
script_button = QPushButton('Run Test Script')
script_button.clicked.connect(on_test_script_push)
extra_button = QPushButton('Extra Button')
extra_button.clicked.connect(on_extra_push)
exit_button = QPushButton('Exit')
exit_button.clicked.connect(on_exit_push)

# Add buttons 
layout.addWidget(script_button)
layout.addWidget(extra_button)
layout.addWidget(exit_button)

# Set layout
window.setLayout(layout)
window.show()
app.exec_()
