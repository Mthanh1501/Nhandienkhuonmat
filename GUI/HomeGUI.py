from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt

class HomeGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a home panel widget
        self.setFixedSize(1080, 657)
        self.move(0, 64)

        homePanel = QWidget(self)  # Specify parent widget
        homePanel.setStyleSheet("background-color: #D9D9D9;")
        homePanel.setFixedSize(954, 531)
        homePanel.move(70, 61)

        # Create a grid layout for panels
        grid_layout = QGridLayout(homePanel)
        # grid_layout.setSpacing(50)  # Set spacing between panels

        # Set minimum width for the first column
        grid_layout.setColumnMinimumWidth(0, 200)
        # Set minimum width for the second column
        # grid_layout.setColumnMinimumWidth(1, 200)

        # Check in
        self.panelCI = QWidget()
        self.panelCI.setFixedSize(200, 100)
        self.panelCI.setStyleSheet("QWidget {border-radius: 5px;background-color: white;}"
                              "QWidget:hover {background-color: #CDCDCD;}")
        label_CI = QLabel("Chấm Công", self.panelCI)
        label_CI.setFixedSize(200, 100)
        label_CI.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.panelCI)

        