from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit,QCheckBox,QComboBox,QCalendarWidget,QDateEdit
from PyQt6.QtCore import Qt,QDate,QTime
from datetime import datetime

from DTO.Staff import Staff
from DTO.Position import Position
from DTO.Checkin import Checkin
from DTO.Checkout import Checkout
from DAO.DBConnect import DBConnect

class SalaryDetailGUI(QWidget):
    salary_list = []
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a login panel widget
        self.setFixedSize(634, 720)

        SalaryDetailPanel = QWidget(self)  # Specify parent widget
        SalaryDetailPanel.setStyleSheet("background-color: #B8B8B8;")
        SalaryDetailPanel.setFixedSize(634, 720)

        # mã nhân viên
        maNVLabel = QLabel("Mã nhân viên", SalaryDetailPanel)
        maNVLabel.setStyleSheet("font-size: 16pt;")
        maNVLabel.setGeometry(26, 31, 291, 30)

        self.maNVInput = QLineEdit(SalaryDetailPanel)
        self.maNVInput.setStyleSheet("""
                background-color: #ccc;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                color: #333;""")
        self.maNVInput.setGeometry(26, 72, 300, 35)
        self.maNVInput.setReadOnly(True)

        # tên nhân viên
        tenNVLabel = QLabel("Tên nhân viên", SalaryDetailPanel)
        tenNVLabel.setStyleSheet("font-size: 16pt;")
        tenNVLabel.setGeometry(26, 130, 291, 30)

        self.tenNVInput = QLineEdit(SalaryDetailPanel)
        self.tenNVInput.setStyleSheet("""
                background-color: #ccc;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                color: #333;""")
        self.tenNVInput.setGeometry(26, 171, 300, 35)
        self.tenNVInput.setReadOnly(True)

        # tên chức vụ
        tenCVLabel = QLabel("Chức vụ", SalaryDetailPanel)
        tenCVLabel.setStyleSheet("font-size: 16pt;")
        tenCVLabel.setGeometry(26, 229, 291, 30)

        self.tenCVInput = QLineEdit(SalaryDetailPanel)
        self.tenCVInput.setStyleSheet("""
                background-color: #ccc;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                color: #333;""")
        self.tenCVInput.setGeometry(26, 270, 300, 35)
        self.tenCVInput.setReadOnly(True)

        # Ngày làm việc
        ngayLamLabel = QLabel("Ngày làm", SalaryDetailPanel)
        ngayLamLabel.setStyleSheet("font-size: 16pt;")
        ngayLamLabel.setGeometry(26, 328, 291, 30)
        
        self.ngayLamInput = QLineEdit(SalaryDetailPanel)
        self.ngayLamInput.setStyleSheet("""
                background-color: #ccc;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                color: #333;""")
        self.ngayLamInput.setGeometry(26, 369, 200, 35)
        self.ngayLamInput.setReadOnly(True)

        # Tổng tiền
        totalLabel = QLabel("Tổng tiền", SalaryDetailPanel)
        totalLabel.setStyleSheet("font-size: 16pt;")
        totalLabel.setGeometry(26, 420, 291, 30)
        
        self.totalInput = QLineEdit(SalaryDetailPanel)
        self.totalInput.setStyleSheet("""
                background-color: #ccc;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                color: #333;""")
        self.totalInput.setGeometry(26, 461, 300, 35)
        self.totalInput.setReadOnly(True)

        # Giờ vào
        timeInLabel = QLabel("Giờ vào", SalaryDetailPanel)
        timeInLabel.setStyleSheet("font-size: 16pt;")
        timeInLabel.setGeometry(369, 328, 291, 30)
        
        self.timeInInput = QLineEdit(SalaryDetailPanel)
        self.timeInInput.setStyleSheet("""
                background-color: #ccc;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                color: #333;""")
        self.timeInInput.setGeometry(369, 360, 200, 35)
        self.timeInInput.setReadOnly(True)

        # Giờ ra
        timeOutLabel = QLabel("Giờ ra", SalaryDetailPanel)
        timeOutLabel.setStyleSheet("font-size: 16pt;")
        timeOutLabel.setGeometry(369, 420, 291, 30)

        self.timeOutInput = QLineEdit(SalaryDetailPanel)
        self.timeOutInput.setStyleSheet("""
                background-color: #ccc;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                color: #333;""")
        self.timeOutInput.setGeometry(369, 461, 200, 35)
        self.timeOutInput.setReadOnly(True)
        
        # Thoát
        self.cancelButton = QPushButton("Thoát", SalaryDetailPanel)
        self.cancelButton.setGeometry(250, 600, 125, 50)
        self.cancelButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        self.cancelButton.clicked.connect(self.close) 


    def selected_data(self, data):
        db_connector = DBConnect()
        mycursor = db_connector.connect()

        # Kiểm tra nếu kết nối thành công
        if mycursor is not None:
            # Thực hiện truy vấn
            sql = "SELECT staff.maNV, staff.tenNV, position.tenCV, chamcong.vaoCa, chamcong.raCa, staff.Luong \
                   FROM staff inner join position on staff.maCV = position.maCV inner join chamcong on staff.maNV = chamcong.maNV \
                   WHERE staff.maNV = %s"
            mycursor.execute(sql,(data,))
            # Lấy kết quả
            results  = mycursor.fetchall()
            for record in results:
                # maNV, tenNV, tenCV, ngayVao, gioVao, gioRa, Luong = record
                # to_str_giovao = str(gioVao)
                # to_str_giora = str(gioRa)
                
                # datetime_giovao = datetime.strptime(to_str_giovao, '%H:%M:%S')
                # datetime_giora = datetime.strptime(to_str_giora, '%H:%M:%S')
                
                # timein = QTime(datetime_giovao.hour, datetime_giovao.minute, datetime_giovao.second)
                # timeout = QTime(datetime_giora.hour, datetime_giora.minute, datetime_giora.second)
                
                # tongGio = timein.secsTo(timeout) / 3600
                
                # tongTien = tongGio * Luong
                
                # self.salary_list.append((maNV, tenNV, tenCV, ngayVao, gioVao, gioRa, tongTien))

                maNV, tenNV, tenCV, vaoCa, raCa, Luong = record
                
                if vaoCa is not None and raCa is not None:
                    to_str_giovao = str(vaoCa)
                    to_str_giora = str(raCa)
                    
                    datetime_vaoCa = datetime.strptime(to_str_giovao, '%Y-%m-%d %H:%M:%S')
                    datetime_raCa = datetime.strptime(to_str_giora, '%Y-%m-%d %H:%M:%S')
                
                    timein = QTime(datetime_vaoCa.hour, datetime_vaoCa.minute, datetime_vaoCa.second)
                    timeout = QTime(datetime_raCa.hour, datetime_raCa.minute, datetime_raCa.second)
                    
                    giovao = datetime_vaoCa.hour
                    phutvao = datetime_vaoCa.minute
                    giayvao = datetime_vaoCa.second
                    
                    giora = datetime_raCa.hour
                    phutra = datetime_raCa.minute
                    giayra = datetime_raCa.second
                    
                    str_giovao = str(giovao) + ":" + str(phutvao) + ":" + str(giayvao)
                    
                    str_giora = str(giora) + ":" + str(phutra) + ":" + str(giayra)
                    
                    ngayVao = datetime_vaoCa.date()
                    
                    tongGio = timein.secsTo(timeout) / 3600
                    
                    tongTien = round((tongGio * Luong), 2)
                    
                    # self.salary_list.append((maNV, tenNV, tenCV, ngayVao, Luong, tongTien))
                    self.salary_list.append((maNV, tenNV, tenCV, ngayVao, str_giovao, str_giora, tongTien))
                else:
                    pass
            # Đóng kết nối sau khi hoàn thành


            if len(self.salary_list) > 0:
                data = self.salary_list[0]
                self.maNVInput.setText(str(data[0]))
                self.tenNVInput.setText(data[1])
                self.tenCVInput.setText(data[2])
                self.ngayLamInput.setText(str(data[3]))
                self.timeInInput.setText(str(data[4]))
                self.timeOutInput.setText(str(data[5]))
                self.totalInput.setText(str(data[6]))

            db_connector.close()
        else:
            print("Failed to connect to database")

    def closeEvent(self, event):
        # Gọi hàm để thực hiện các thao tác sau khi cửa sổ được đóng
        self.on_window_close()

    def on_window_close(self):
        # Thực hiện các thao tác sau khi cửa sổ được đóng
        self.salary_list.clear()

    def showCancelButton(self):
        self.cancelButton.show()

