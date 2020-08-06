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

        input_widget = QWidget(self)
        sat1 = QFormLayout()
        sat2 = QFormLayout()

        apo_label = QLabel("Apoapsis to surface:")
        apo_label.setStyleSheet("color: white")
        apo_label.setFont(QFont('Arial', 14))
        apo_label.setAttribute(Qt.WA_TranslucentBackground)

        peri_label = QLabel("Periapsis to surface:")
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

        sat1.addRow(header1)
        sat1.addRow(apo_label, self.apo_1)
        sat1.addRow(peri_label, self.peri_1)
        sat1.addRow(pos_label, self.pos_1)
        sat1.addRow(bapo_label, self.bapo_1)
        sat1.setVerticalSpacing(20)

        apo_label = QLabel("Apoapsis to surface:")
        apo_label.setStyleSheet("color: white")
        apo_label.setFont(QFont('Arial', 14))
        apo_label.setAttribute(Qt.WA_TranslucentBackground)

        peri_label = QLabel("Periapsis to surface:")
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

        footer = QLabel("*Leave Blank")

        sat2.addRow(header2)
        sat2.addRow(apo_label, self.apo_2)
        sat2.addRow(peri_label, self.peri_2)
        sat2.addRow(pos_label, self.pos_2)
        sat2.addRow(bapo_label, self.bapo_2)
        sat2.setVerticalSpacing(20)


        container = QHBoxLayout()
        container.addItem(sat1)
        container.addItem(sat2)
        container.setSpacing(25)
        input_widget.setLayout(container)





        return input_widget



    def graph_buttons(self):
        button_box = QDialogButtonBox(Qt.Horizontal) #QHBoxLayout()
        plot_orbit = self.create_button("Graph Orbits")
        ani_orbit = self.create_button('Animate Orbits')
        plot_torbit = self.create_button('Graph Transfer Orbits')
        ani_torbit = self.create_button('Animate Transfer Orbits')
        '''button_box.addWidget(plot_orbit)
        button_box.addWidget(ani_orbit)
        button_box.addWidget(plot_torbit)
        button_box.addWidget(ani_torbit)'''
        button_box.addButton(plot_orbit, QDialogButtonBox.ActionRole)
        button_box.addButton(ani_orbit, QDialogButtonBox.ActionRole)
        button_box.addButton(plot_torbit, QDialogButtonBox.ActionRole)
        button_box.addButton(ani_torbit, QDialogButtonBox.ActionRole)
        return button_box

    @pyqtSlot()
    def on_begin(self):
        self.setFixedSize(1000,700)
        self.center()




        # Button Box
        self.begin.deleteLater()



        buttons = self.graph_buttons()
        sats = self.init_inputs()
        sat_titles = QHBoxLayout()


        layout = QGridLayout() #QVBoxLayout()
        layout.addWidget(sats, 1,0)
        layout.addWidget(buttons, 2,0)



        self.contentContainer.setLayout(layout)
        self.setCentralWidget(self.contentContainer)
        #self.button_box.setGeometry(50, 250, 400, 300)
        self.show()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
