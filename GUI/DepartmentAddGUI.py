from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QLineEdit,QCheckBox,QComboBox,QCalendarWidget,QDateEdit,QToolButton,QMessageBox
from PyQt6.QtCore import Qt,QDate

from DAO.DepartmentDAO import  DepartmentDAO
from DAO import DBConnect
from DTO import Department

class DepartmentAddGUI(QWidget):
    # staff_list = []
    # PB_list = []
    # CV_list = []
    department_list = []

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a login panel widget
        self.setFixedSize(350, 321)

        DepartmentAddPanel = QWidget(self)  # Specify parent widget
        DepartmentAddPanel.setStyleSheet("background-color: #B8B8B8;")
        DepartmentAddPanel.setFixedSize(634, 720)

        # mã phòng ban
        maPBLabel = QLabel("Mã phòng ban", DepartmentAddPanel)
        maPBLabel.setStyleSheet("font-size: 16pt;")
        maPBLabel.setGeometry(26, 31, 291, 30)
        maPBLabel.setVisible(False)

        self.maPBInput = QLineEdit(DepartmentAddPanel)
        self.maPBInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                display: none;""")
        self.maPBInput.setGeometry(26, 72, 300, 35)
        self.maPBInput.setVisible(False)

        # tên phòng ban
        tenPBLabel = QLabel("Tên phòng ban", DepartmentAddPanel)
        tenPBLabel.setStyleSheet("font-size: 16pt;")
        tenPBLabel.setGeometry(26, 31, 291, 30)

        self.tenPBInput = QLineEdit(DepartmentAddPanel)
        self.tenPBInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.tenPBInput.setGeometry(26, 72, 300, 35)

        # Địa điểm phòng ban
        ddLabel = QLabel("Địa điểm phòng ban", DepartmentAddPanel)
        ddLabel.setStyleSheet("font-size: 16pt;")
        ddLabel.setGeometry(26, 130, 291, 30)

        self.ddInput = QLineEdit(DepartmentAddPanel)
        self.ddInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.ddInput.setGeometry(26, 171, 300, 35)

        # Thêm
        self.addButton = QPushButton("Thêm", DepartmentAddPanel)
        self.addButton.setGeometry(117, 250, 125, 50)
        self.addButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        
        self.addButton.clicked.connect(self.addPB)
    

    def addPB(self):
        maPB = self.maPBInput.text()
        tenPB = self.tenPBInput.text()
        ddiem = self.ddInput.text()
        self.dpm_dao = DepartmentDAO()
        self.dpm_dao.add(maPB, tenPB, ddiem)
        self.close()

            
