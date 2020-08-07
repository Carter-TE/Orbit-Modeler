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

        #Planet input fields
        self.mass = QLineEdit()
        self.mass.setStyleSheet("background: white")
        self.radius = QLineEdit()
        self.radius.setStyleSheet("background: white")


        # Sat 1 input fields
        self.apo_1 = QLineEdit()
        self.apo_1.setStyleSheet("background: white")
        self.peri_1 = QLineEdit()
        self.peri_1.setStyleSheet("background: white")
        self.pos_1 = QLineEdit()
        self.pos_1.setStyleSheet("background: white")
        self.bapo_1 = QComboBox()
        self.bapo_1.addItem("Yes")
        self.bapo_1.addItem("No")
        self.bapo_1.setFixedSize(80,30)
        self.bapo_1.setStyleSheet("background: white")

        # Sat 2 input fields
        self.apo_2 = QLineEdit()
        self.apo_2.setStyleSheet("background: white")
        self.peri_2 = QLineEdit()
        self.peri_2.setStyleSheet("background: white")
        self.pos_2 = QLineEdit()
        self.pos_2.setStyleSheet("background: white")
        self.bapo_2 = QComboBox()
        self.bapo_2.addItem("Yes")
        self.bapo_2.addItem("No")
        self.bapo_2.setFixedSize(80,30)
        self.bapo_2.setStyleSheet("background: white")

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

        # Begin button
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

    # Initializes satellite 1 input form
    def sat1_inputs(self):
        sat1 = QFormLayout()

        apo_label = QLabel("Apoapsis to surface: ")
        apo_label.setStyleSheet("color: white")
        apo_label.setFont(QFont('Arial', 14))
        apo_label.setAttribute(Qt.WA_TranslucentBackground)

        peri_label = QLabel("Periapsis to surface: ")
        peri_label.setStyleSheet("color: white")
        peri_label.setFont(QFont('Arial', 14))
        peri_label.setAttribute(Qt.WA_TranslucentBackground)

        pos_label = QLabel("Initial position:")
        pos_label.setStyleSheet("color: white")
        pos_label.setFont(QFont('Arial', 14))
        pos_label.setAttribute(Qt.WA_TranslucentBackground)

        bapo_label = QLabel("Before Apoapsis")
        bapo_label.setStyleSheet("color: white")
        bapo_label.setFont(QFont('Arial', 14))
        bapo_label.setAttribute(Qt.WA_TranslucentBackground)

        header1 = QLabel("Satellite 1")
        header1.setStyleSheet("color: white")
        header1.setFont(QFont('Arial', 16))
        header1.setAttribute(Qt.WA_TranslucentBackground)

        sat1.addRow(header1)
        sat1.addRow(apo_label, self.apo_1)
        sat1.addRow(peri_label, self.peri_1)
        sat1.addRow(pos_label, self.pos_1)
        sat1.addRow(bapo_label, self.bapo_1)
        sat1.setVerticalSpacing(20)


        return sat1

    # Initializes satellite 2 input form
    def sat2_inputs(self):
        sat2 = QFormLayout()

        apo_label = QLabel("Apoapsis to surface: ")
        apo_label.setStyleSheet("color: white")
        apo_label.setFont(QFont('Arial', 14))
        apo_label.setAttribute(Qt.WA_TranslucentBackground)

        peri_label = QLabel("Periapsis to surface: ")
        peri_label.setStyleSheet("color: white")
        peri_label.setFont(QFont('Arial', 14))
        peri_label.setAttribute(Qt.WA_TranslucentBackground)

        pos_label = QLabel("Initial position:")
        pos_label.setStyleSheet("color: white")
        pos_label.setFont(QFont('Arial', 14))
        pos_label.setAttribute(Qt.WA_TranslucentBackground)

        bapo_label = QLabel("Before Apoapsis")
        bapo_label.setStyleSheet("color: white")
        bapo_label.setFont(QFont('Arial', 14))
        bapo_label.setAttribute(Qt.WA_TranslucentBackground)

        header2 = QLabel("Satellite 2")
        header2.setStyleSheet("color: white")
        header2.setFont(QFont('Arial', 16))
        header2.setAttribute(Qt.WA_TranslucentBackground)

        sat2.addRow(header2)
        sat2.addRow(apo_label, self.apo_2)
        sat2.addRow(peri_label, self.peri_2)
        sat2.addRow(pos_label, self.pos_2)
        sat2.addRow(bapo_label, self.bapo_2)
        sat2.setVerticalSpacing(20)

        return sat2

    # Initializes parent body input form
    def planet_inputs(self):

        planet = QFormLayout()

        header = QLabel("Parent Body")
        header.setStyleSheet("color: white")
        header.setFont(QFont('Arial', 16))

        mass_l = QLabel("Mass: ")
        mass_l.setStyleSheet("color: white")
        mass_l.setFont(QFont('Arial', 16))

        rad_l = QLabel("Radius: ")
        rad_l.setStyleSheet("color: white")
        rad_l.setFont(QFont('Arial', 16))

        planet.addRow(header)
        planet.addRow(mass_l, self.mass)
        planet.addRow(rad_l, self.radius)
        planet.setVerticalSpacing(20)

        return planet

    # Creates Button box for graphing options
    def graph_buttons(self):
        button_box = QDialogButtonBox(Qt.Horizontal) #QHBoxLayout()
        plot_orbit = self.create_button("Graph Orbits")
        ani_orbit = self.create_button('Animate Orbits')
        plot_torbit = self.create_button('Graph Transfer Orbits')
        ani_torbit = self.create_button('Animate Transfer Orbits')
        button_box.addButton(plot_orbit, QDialogButtonBox.ActionRole)
        button_box.addButton(ani_orbit, QDialogButtonBox.ActionRole)
        button_box.addButton(plot_torbit, QDialogButtonBox.ActionRole)
        button_box.addButton(ani_torbit, QDialogButtonBox.ActionRole)
        return button_box

    # Creates second menu
    def init_inputs_window(self):
        self.setFixedSize(1000, 700)
        self.center()

        self.begin.deleteLater()

        sats_container = QHBoxLayout()
        sats_container.addItem(self.sat1_inputs())
        sats_container.addItem(self.sat2_inputs())

        input_container = QVBoxLayout()
        input_container.addItem(self.planet_inputs())
        input_container.addItem(sats_container)

        buttons = self.graph_buttons()

        container = QVBoxLayout()
        container.addItem(input_container)
        container.addWidget(buttons)

        self.contentContainer.setLayout(container)
        self.setCentralWidget(self.contentContainer)

        self.show()


    @pyqtSlot()
    def on_begin(self):
        self.init_inputs_window()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
