from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit,QCheckBox,QComboBox,QCalendarWidget,QDateEdit,QMessageBox
from PyQt6.QtCore import Qt,QDate

from DAO.PositionDAO import  PositionDAO
from DAO.DBConnect import DBConnect
from DTO import Position

class PositionDetailGUI(QWidget):
    # staff_list = []
    # PB_list = []
    # CV_list = []
    
    position_list = []
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a login panel widget
        self.setFixedSize(634, 720)

        PositionDetailPanel = QWidget(self)  # Specify parent widget
        PositionDetailPanel.setStyleSheet("background-color: #B8B8B8;")
        PositionDetailPanel.setFixedSize(634, 720)

        # mã chức vụ
        maCVLabel = QLabel("Mã chức vụ", PositionDetailPanel)
        maCVLabel.setStyleSheet("font-size: 16pt;")
        maCVLabel.setGeometry(26, 31, 291, 30)

        self.maCVInput = QLineEdit(PositionDetailPanel)
        self.maCVInput.setStyleSheet("""
                background-color: #ccc;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                color: #333;""")
        self.maCVInput.setGeometry(26, 72, 300, 35)
        self.maCVInput.setReadOnly(True)

        # tên chức vụ
        tenCVLabel = QLabel("Tên chức vụ", PositionDetailPanel)
        tenCVLabel.setStyleSheet("font-size: 16pt;")
        tenCVLabel.setGeometry(26, 130, 291, 30)

        self.tenCVInput = QLineEdit(PositionDetailPanel)
        self.tenCVInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.tenCVInput.setGeometry(26, 171, 300, 35)

        # Hủy
        self.cancelButton = QPushButton("Hủy", PositionDetailPanel)
        self.cancelButton.setGeometry(112, 600, 125, 50)
        self.cancelButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        self.cancelButton.clicked.connect(self.close) 
        
        # Cập nhật
        self.updateButton = QPushButton("Lưu", PositionDetailPanel)
        self.updateButton.setGeometry(389, 600, 125, 50)
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
            sql = "SELECT * from position where maCV = %s"
            mycursor.execute(sql,(data,))
            # Lấy kết quả
            results  = mycursor.fetchall()
            for record in results:
                maCV, tenCV = record
                position = Position.Position(maCV, tenCV)
                self.position_list.append(position)
            # Đóng kết nối sau khi hoàn thành

            self.maCVInput.setText(str(position.getMaCV()))
            self.tenCVInput.setText(position.getTenCV())
            
            db_connector.close()
        else:
            print("Failed to connect to database")

    def updateDB(self):
        maCV = self.maCVInput.text()
        tenCV = self.tenCVInput.text()

        self.pos_dao = PositionDAO()
        self.pos_dao.update(maCV, tenCV)

    def showCancelButton(self):
        self.cancelButton.show()
