import Satellite
import OrbitalGraph as grapher
import math
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Orbit Simulator v.2.3'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 500
        self.init_UI()

    def init_UI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.center()
        self.setStyleSheet("background-image: url(Moon.jpg)")

        # Title label
        header = QLabel(self)
        header.setText("Orbit Simulator")
        header_font = QFont('Arial', 24)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setStyleSheet("color: white")
        header.setAttribute(Qt.WA_TranslucentBackground)
        header.setGeometry(70,50,400,200)

        # Buttons
        plot_orbit = self.create_button("Graph Orbits")
        ani_orbit = self.create_button('Animate Orbits')
        plot_torbit = self.create_button('Graph Transfer Orbits')
        ani_torbit = self.create_button('Animate Transfer Orbits')

        # Button Box
        button_box = QDialogButtonBox(Qt.Vertical, self)
        button_box.addButton(plot_orbit, QDialogButtonBox.ActionRole)
        button_box.addButton(ani_orbit, QDialogButtonBox.ActionRole)
        button_box.addButton(plot_torbit, QDialogButtonBox.ActionRole)
        button_box.addButton(ani_torbit, QDialogButtonBox.ActionRole)
        button_box.setGeometry(50,250,400,300)

        self.show()

    # Helper method to center main window
    def center(self):
        d = self.frameGeometry()
        cd = QDesktopWidget().availableGeometry().center()
        d.moveCenter(cd)
        print(d.topLeft())
        self.move(d.topLeft())

    # Helper method to create buttons
    def create_button(self, label):
        button = QPushButton(label, self)
        button.setStyleSheet("color: white")
        button.setFont(QFont('Arial', 14))
        return button



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
