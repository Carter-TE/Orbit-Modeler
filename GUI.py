import Satellite
import OrbitalGraph as grapher
import math
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot
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

        self.window_layout = QVBoxLayout()
        self.contentContainer = QWidget()


        self.button_box = QDialogButtonBox(Qt.Horizontal, self)


        # Sat 1 input fields
        self.apo_1 = QLineEdit()
        self.peri_1 = QLineEdit()
        self.pos_1 = QLineEdit()
        self.bapo_1 = QLineEdit()

        # Sat 2 input fields
        self.apo_2 = QLineEdit()
        self.peri_2 = QLineEdit()
        self.pos_2 = QLineEdit()
        self.bapo_2 = QLineEdit()


        self.init_UI()

    def init_UI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.center()
        print(self.updatesEnabled())
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
        self.begin = self.create_button("Begin")
        self.begin.clicked.connect(self.on_begin)
        self.begin.setGeometry(200,250,100,50)


        self.show()

    # Helper method to center main window
    def center(self):
        d = self.frameGeometry()
        cd = QDesktopWidget().availableGeometry().center()
        d.moveCenter(cd)
        self.move(d.topLeft())

    # Helper method to create buttons
    def create_button(self, label):
        button = QPushButton(label, self)
        button.setStyleSheet("color: white")
        button.setFont(QFont('Arial', 14))
        return button

    def init_inputs(self):
        layout = QHBoxLayout()

        sat1 = QFormLayout
        sat1.addRow(QLabel("Enter distance from Apoapsis to surface"), self.apo_1)
        '''sat1.addRow("Enter distance from Periapsis to surface", self.peri_1)
        sat1.addRow("Enter satellites initial position", self.pos_1)
        sat1.addRow("Is satellite before apoapsis", self.bapo_1)'''



        return layout

    def graph_buttons(self):
        button_box = QHBoxLayout()
        plot_orbit = self.create_button("Graph Orbits")
        ani_orbit = self.create_button('Animate Orbits')
        plot_torbit = self.create_button('Graph Transfer Orbits')
        ani_torbit = self.create_button('Animate Transfer Orbits')
        button_box.addWidget(plot_orbit)
        button_box.addWidget(ani_orbit)
        button_box.addWidget(plot_torbit)
        button_box.addWidget(ani_torbit)
        return button_box

    @pyqtSlot()
    def on_begin(self):
        self.setFixedSize(1000,700)





        # Button Box
        self.begin.deleteLater()



        buttons = self.graph_buttons()
        layout = QVBoxLayout()
        layout.addItem(buttons)


        self.contentContainer.setLayout(layout)
        self.setCentralWidget(self.contentContainer)
        #self.button_box.setGeometry(50, 250, 400, 300)
        self.show()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
