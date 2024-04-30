from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt


class HeaderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Tạo các phần tử UI cho header ở đây
        header = QWidget(self)
        header.setStyleSheet("background-color: white;")
        header.setFixedSize(1080, 64)

        self.label = QLabel("Welcome!!", header)
        self.label.setStyleSheet("font-size: 20pt;")
        self.label.setGeometry(17, 11, 500, 39)

        self.login_button = QPushButton("Đăng nhập", header)
        self.login_button.setFixedSize(115, 26)
        self.login_button.move(946, 19)
        self.login_button.setStyleSheet("QPushButton {border-radius: 5px;background-color: #D9D9D9;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #CDCDCD;}"
                                        "QPushButton:pressed {background-color: darkgray;}")
