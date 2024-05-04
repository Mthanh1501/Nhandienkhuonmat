from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit,QCheckBox,QComboBox,QCalendarWidget,QDateEdit,QMessageBox
from PyQt6.QtCore import Qt,QDate

from DAO.DepartmentDAO import  DepartmentDAO
from DAO.DBConnect import DBConnect
from DTO import Department

class DepartmentDetailGUI(QWidget):
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

        DepartmentDetailPanel = QWidget(self)  # Specify parent widget
        DepartmentDetailPanel.setStyleSheet("background-color: #B8B8B8;")
        DepartmentDetailPanel.setFixedSize(634, 720)

        # mã phòng ban
        maPBLabel = QLabel("Mã phòng ban", DepartmentDetailPanel)
        maPBLabel.setStyleSheet("font-size: 16pt;")
        maPBLabel.setGeometry(26, 31, 291, 30)

        self.maPBInput = QLineEdit(DepartmentDetailPanel)
        self.maPBInput.setStyleSheet("""
                background-color: #ccc;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                color: #333;""")
        self.maPBInput.setGeometry(26, 72, 300, 35)
        self.maPBInput.setReadOnly(True)

        # tên phòng ban
        tenPBLabel = QLabel("Tên phòng ban", DepartmentDetailPanel)
        tenPBLabel.setStyleSheet("font-size: 16pt;")
        tenPBLabel.setGeometry(26, 31, 291, 30)

        self.tenPBInput = QLineEdit(DepartmentDetailPanel)
        self.tenPBInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.tenPBInput.setGeometry(26, 72, 300, 35)

        # Địa điểm phòng ban
        ddLabel = QLabel("Địa điểm phòng ban", DepartmentDetailPanel)
        ddLabel.setStyleSheet("font-size: 16pt;")
        ddLabel.setGeometry(26, 130, 291, 30)

        self.ddInput = QLineEdit(DepartmentDetailPanel)
        self.ddInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.ddInput.setGeometry(26, 171, 300, 35)
        
        # Hủy
        self.cancelButton = QPushButton("Hủy", DepartmentDetailPanel)
        self.cancelButton.setGeometry(34, 230, 125, 50)
        self.cancelButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        self.cancelButton.clicked.connect(self.close) 
        
        # Cập nhật
        self.updateButton = QPushButton("Lưu", DepartmentDetailPanel)
        self.updateButton.setGeometry(200, 230, 125, 50)
        self.updateButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        self.updateButton.clicked.connect(self.updateDB)

    def selected_data(self, data):
        db_connector = DBConnect()
        mycursor = db_connector.connect()

        # Kiểm tra nếu kết nối thành công
        if mycursor is not None:
            # Thực hiện truy vấn
            sql = "SELECT * from department where maPB = %s"
            mycursor.execute(sql,(data,))
            # Lấy kết quả
            results  = mycursor.fetchall()
            for record in results:
                maPB, tenPB, diaDiem = record
                department = Department.Department(maPB, tenPB, diaDiem)
                self.department_list.append(department)
            # Đóng kết nối sau khi hoàn thành

            self.maPBInput.setText(str(department.getMaPB()))
            self.tenPBInput.setText(department.getTenPB())
            self.ddInput.setText(department.getDiaDiemPB())

            db_connector.close()
        else:
            print("Failed to connect to database")

    def updateDB(self):
        maPB = self.maPBInput.text()
        tenPB = self.tenPBInput.text()
        diaDiem = self.ddInput.text()

        self.dpm_dao = DepartmentDAO()
        self.dpm_dao.update(maPB, tenPB, diaDiem)
        self.close()


    def showCancelButton(self):
        self.cancelButton.show()
