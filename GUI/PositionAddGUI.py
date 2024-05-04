from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QLineEdit,QCheckBox,QComboBox,QCalendarWidget,QDateEdit,QToolButton, QMessageBox
from PyQt6.QtCore import Qt,QDate

from DAO.PositionDAO import  PositionDAO
from DAO import DBConnect
from DTO import Position

class PositionAddGUI(QWidget):
    # staff_list = []
    # PB_list = []
    # CV_list = []
    position_list = []

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a login panel widget
        self.setFixedSize(550, 400)

        PositionAddPanel = QWidget(self)  # Specify parent widget
        PositionAddPanel.setStyleSheet("background-color: #B8B8B8;")
        PositionAddPanel.setFixedSize(550, 400)

        # mã chức vụ
        maCVLabel = QLabel("Mã chức vụ", PositionAddPanel)
        maCVLabel.setStyleSheet("font-size: 16pt;")
        maCVLabel.setGeometry(26, 31, 291, 30)
        maCVLabel.setVisible(False)

        self.maCVInput = QLineEdit(PositionAddPanel)
        self.maCVInput.setStyleSheet("""
                background-color: #ccc;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                color: #333;""")
        self.maCVInput.setGeometry(35, 72, 300, 35)
        self.maCVInput.setVisible(False)

        # tên chức vụ
        tenCVLabel = QLabel("Tên chức vụ", PositionAddPanel)
        tenCVLabel.setStyleSheet("font-size: 16pt;")
        tenCVLabel.setGeometry(120, 130, 291, 30)

        self.tenCVInput = QLineEdit(PositionAddPanel)
        self.tenCVInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.tenCVInput.setGeometry(120, 171, 300, 35)

        # Thêm
        self.addButton = QPushButton("Thêm", PositionAddPanel)
        self.addButton.setGeometry(200, 280, 125, 50)
        self.addButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        
        self.addButton.clicked.connect(self.addPB)
    

    def addPB(self):
        maCV = self.maCVInput.text()
        tenCV = self.tenCVInput.text()
        self.pos_dao = PositionDAO()
        self.pos_dao.add(maCV, tenCV)
        self.close()

            
