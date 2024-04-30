from PyQt6.QtWidgets import QFileDialog,QWidget, QLabel, QPushButton, QApplication, QLineEdit,QCheckBox,QComboBox,QCalendarWidget,QDateEdit,QToolButton,QMessageBox
from PyQt6.QtCore import Qt,QDate
from PyQt6.QtCore import QByteArray, QBuffer, QIODevice
from PyQt6.QtGui import QPixmap

from DAO.StaffDAO import  StaffDAO
from DAO import DBConnect
from DTO import Department,Position

class StaffAddGUI(QWidget):
    staff_list = []
    PB_list = []
    CV_list = []

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a login panel widget
        self.setFixedSize(634, 650)

        StaffAddPanel = QWidget(self)  # Specify parent widget
        StaffAddPanel.setStyleSheet("background-color: #B8B8B8;")
        StaffAddPanel.setFixedSize(634, 720)

        # mã nhân viên
        maNVLabel = QLabel("Mã nhân viên", StaffAddPanel)
        maNVLabel.setStyleSheet("font-size: 16pt;")
        maNVLabel.setGeometry(26, 31, 291, 30)
        maNVLabel.setVisible(False)

        self.maNVInput = QLineEdit(StaffAddPanel)
        self.maNVInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                """)
        self.maNVInput.setGeometry(26, 72, 300, 35)
        self.maNVInput.setVisible(False)


        # tên nhân viên
        tenNVLabel = QLabel("Tên nhân viên", StaffAddPanel)
        tenNVLabel.setStyleSheet("font-size: 16pt;")
        tenNVLabel.setGeometry(26, 130, 291, 30)

        self.tenNVInput = QLineEdit(StaffAddPanel)
        self.tenNVInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.tenNVInput.setGeometry(26, 171, 300, 35)

        # avata
        self.avataLabel = QLabel(StaffAddPanel)
        self.avataLabel.setStyleSheet("background-color: white; border: 1px solid black;")
        self.avataLabel.setGeometry(397, 31, 171, 228)

        file_path = "Icons/icon_avata.jpg"
        self.pixmap = QPixmap(file_path)
        
        # Hiển thị hình ảnh trên QLabel
        self.avataLabel.setPixmap(self.pixmap.scaled(self.avataLabel.size(), Qt.AspectRatioMode.KeepAspectRatio))

        self.faceButton = QPushButton("Chọn ảnh", StaffAddPanel)
        self.faceButton.setGeometry(432, 270, 101, 33)
        self.faceButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: #9F9B9B;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #CDCDCD;}"
                                        "QPushButton:pressed {background-color: darkgray;}")
        
        self.faceButton.clicked.connect(self.open_image)

        # Số điện thoại
        sDTLabel = QLabel("Số điện thoại", StaffAddPanel)
        sDTLabel.setStyleSheet("font-size: 16pt;")
        sDTLabel.setGeometry(26, 229, 291, 30)

        self.sDTInput = QLineEdit(StaffAddPanel)
        self.sDTInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.sDTInput.setGeometry(26, 270, 300, 35)

        # Ngày sinh
        ngaySinhLabel = QLabel("Ngày sinh", StaffAddPanel)
        ngaySinhLabel.setStyleSheet("font-size: 16pt;")
        ngaySinhLabel.setGeometry(26, 328, 291, 30)

        self.ngaySinhInput = QDateEdit(StaffAddPanel)
        self.ngaySinhInput.setDisplayFormat("dd/MM/yy")
        self.ngaySinhInput.setDate(QDate.currentDate())
        self.ngaySinhInput.setGeometry(26, 369, 106, 35)
        self.ngaySinhInput.setCalendarPopup(True)
        self.ngaySinhInput.setStyleSheet("""
            QDateEdit {
                background-color: White;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                padding-left: 5px;
            }    
            QToolButton {
                background-color: white; /* Màu nền của các nút */
                color: black; /* Màu chữ của các nút */
            }
        """)
        # Thiết lập cửa sổ lịch tùy chỉnh
        custom_calendar = CustomCalendarWidget()
        self.ngaySinhInput.setCalendarWidget(custom_calendar)
        
        # giới tính
        gioiTinhLabel = QLabel("Giới tính", StaffAddPanel)
        gioiTinhLabel.setStyleSheet("font-size: 16pt;")
        gioiTinhLabel.setGeometry(160, 328, 106, 26)

        self.namCB = QCheckBox("Nam", StaffAddPanel)
        self.namCB.setStyleSheet("font-size: 16pt;")
        self.namCB.move(157, 370)
        self.namCB.clicked.connect(self.handleNamCheckbox)

        self.nuCB = QCheckBox("Nữ", StaffAddPanel)
        self.nuCB.setStyleSheet("font-size: 16pt;")
        self.nuCB.move(250, 370)
        self.nuCB.clicked.connect(self.handleNuCheckbox)

        # phòng ban
        self.list_PB()
        viTriLabel = QLabel("Phòng ban", StaffAddPanel)
        viTriLabel.setStyleSheet("font-size: 16pt;")
        viTriLabel.setGeometry(26, 420, 291, 30)

        self.viTriComboBox = QComboBox(StaffAddPanel)  # Change to QComboBox
        self.viTriComboBox.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.viTriComboBox.setGeometry(26, 461, 300, 35)
        for vitri in self.PB_list:
            self.viTriComboBox.addItem(vitri.getTenPB())
        self.viTriComboBox.setCurrentIndex(-1)

        # Chức vụ
        self.list_CV()
        chucVuLabel = QLabel("Chức vụ", StaffAddPanel)
        chucVuLabel.setStyleSheet("font-size: 16pt;")
        chucVuLabel.setGeometry(369, 328, 291, 30)

        self.chucVuComboBox = QComboBox(StaffAddPanel)  # Change to QComboBox
        self.chucVuComboBox.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.chucVuComboBox.setGeometry(369, 360, 200, 35)
        for chucvu in self.CV_list:
            self.chucVuComboBox.addItem(chucvu.getTenCV())
        self.chucVuComboBox.setCurrentIndex(-1)

        # luong
        luongLabel = QLabel("Lương", StaffAddPanel)
        luongLabel.setStyleSheet("font-size: 16pt;")
        luongLabel.setGeometry(369, 420, 291, 30)

        self.luongInput = QLineEdit(StaffAddPanel)
        self.luongInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.luongInput.setGeometry(369, 461, 200, 35)

        # Thêm
        self.addButton = QPushButton("Thêm", StaffAddPanel)
        self.addButton.setGeometry(250, 550, 125, 50)
        self.addButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        
        self.addButton.clicked.connect(self.addDB)
    
    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn Ảnh", "", "Image Files (*.png *.jpg *.bmp *.jpeg)")
        
        if file_path:
            self.pixmap = QPixmap(file_path)  # Tải hình ảnh từ đường dẫn tệp được chọn
            scaled_pixmap = self.pixmap.scaled(self.avataLabel.size(), aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio)  # Thay đổi kích thước ảnh nếu cần
            self.avataLabel.setPixmap(scaled_pixmap)  # Đặt hình ảnh vào QLabel
            self.avataLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def list_CV(self):
        # Kết nối đến cơ sở dữ liệu và nhận đối tượng cursor
        db_connector = DBConnect.DBConnect()
        mycursor = db_connector.connect()

        # Kiểm tra nếu kết nối thành công
        if mycursor is not None:
            # Thực hiện truy vấn
            sql = "SELECT * FROM `position`"
            mycursor.execute(sql)
            # Lấy kết quả
            results  = mycursor.fetchall()

            for record in results:
                maCV, tenCV = record
                position = Position.Position(maCV, tenCV)
                self.CV_list.append(position)
            # Đóng kết nối sau khi hoàn thành
            db_connector.close()
        else:
            print("Failed to connect to database")

    def list_PB(self):
        # Kết nối đến cơ sở dữ liệu và nhận đối tượng cursor
        db_connector = DBConnect.DBConnect()
        mycursor = db_connector.connect()

        # Kiểm tra nếu kết nối thành công
        if mycursor is not None:
            # Thực hiện truy vấn
            sql = "SELECT * FROM department;"
            mycursor.execute(sql)
            # Lấy kết quả
            results  = mycursor.fetchall()

            for record in results:
                maPB, tenPB, diaDiemPB = record
                department = Department.Department(maPB, tenPB, diaDiemPB)
                self.PB_list.append(department)
            # Đóng kết nối sau khi hoàn thành
            db_connector.close()
        else:
            print("Failed to connect to database")

    def addDB(self):
        maNV = self.maNVInput.text()
        tenNV = self.tenNVInput.text()
        sDT = self.sDTInput.text()
        ngaySinh = self.ngaySinhInput.date().toString(Qt.DateFormat.ISODate)
        
        if self.viTriComboBox.currentIndex() == -1:
            # Gán giá trị mặc định cho maPB (ví dụ: 0)
            maPB = 0
        else:
            for PB in self.PB_list:
                if PB.getTenPB() == self.viTriComboBox.currentText():
                    maPB = PB.getMaPB()
        
        if not self.namCB.isChecked() and not self.nuCB.isChecked():
            QMessageBox.warning(None, "Nhắc nhở", "Vui lòng chọn giới tính cho nhân viên!")
            return
        else:
            if self.namCB.isChecked():
                gioiTinh = 0
            else: 
                gioiTinh = 1
            
        if self.chucVuComboBox.currentIndex() == -1:
            # Gán giá trị mặc định cho maPB (ví dụ: 0)
            maCV = 0
        else:
            for CV in self.CV_list:
                if CV.getTenCV() == self.chucVuComboBox.currentText():
                    maCV = CV.getMaCV()
        luong = self.luongInput.text()
        trangthai = 1

        # Chuyển đổi QPixmap thành QImage
        image = self.pixmap.toImage()

        # Chuyển đổi QImage thành dữ liệu bytes
        image_data = QByteArray()
        buffer = QBuffer(image_data)
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        image.save(buffer, "jpg")

        self.staff_dao = StaffDAO()

        self.staff_dao.add(maNV, tenNV, sDT, ngaySinh, gioiTinh, maPB, maCV, luong, trangthai,image_data)

        self.close()
        # trả lại giá trị mặc định
        # self.chucVuComboBox.clear()
        # self.viTriComboBox.clear()
        # self.PB_list.clear()
        # self.CV_list.clear()
        

    def closeEvent(self, event):
        # Gọi hàm để thực hiện các thao tác sau khi cửa sổ được đóng
        self.on_window_close()

    def on_window_close(self):
        # Thực hiện các thao tác sau khi cửa sổ được đóng
        self.chucVuComboBox.clear()
        self.viTriComboBox.clear()
        self.PB_list.clear()
        self.CV_list.clear()

    def handleNamCheckbox(self):
        if self.namCB.isChecked():
            self.nuCB.setChecked(False)

    def handleNuCheckbox(self):
        if self.nuCB.isChecked():
            self.namCB.setChecked(False)


# cái này là css cho lịch tại vì ko thể thay đổi trực tiếp được
class CustomCalendarWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("""
            background-color: white; /* Màu nền của cửa sổ lịch */
            color: black; /* Màu chữ của ngày */                        
        """)
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)  # Ẩn cột số tuần (cột bên trái)

    def paintCell(self, painter, rect, date):
        # Gọi phương thức gốc để vẽ ngày
        super().paintCell(painter, rect, date)

        # Kiểm tra xem ngày có thuộc tháng hiện tại hay không
        if date.month() == self.monthShown():
            # Làm mờ chữ của các ngày thuộc tháng hiện tại
            painter.setOpacity(0.5)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(date.day()))