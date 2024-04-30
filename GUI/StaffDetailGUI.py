from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit,QCheckBox,QComboBox,QCalendarWidget,QDateEdit,QMessageBox,QFileDialog
from PyQt6.QtCore import Qt,QDate
from PyQt6.QtCore import QByteArray, QBuffer, QIODevice

from PyQt6.QtGui import QPixmap,QImage,QTransform,QImageReader

from DAO.StaffDAO import  StaffDAO
from DAO.DBConnect import DBConnect
from DTO import Department,Position
from DTO.Staff import Staff

from GUI import FaceRecognitionWidget

class StaffDetailGUI(QWidget):
    staff_list = []
    PB_list = []
    CV_list = []
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        global signedLabel
        # Create a login panel widget
        self.setFixedSize(634, 690)

        StaffAddPanel = QWidget(self)  # Specify parent widget
        StaffAddPanel.setStyleSheet("background-color: #B8B8B8;")
        StaffAddPanel.setFixedSize(634, 720)

        # mã nhân viên
        maNVLabel = QLabel("Mã nhân viên", StaffAddPanel)
        maNVLabel.setStyleSheet("font-size: 16pt;")
        maNVLabel.setGeometry(26, 31, 291, 30)

        self.maNVInput = QLineEdit(StaffAddPanel)
        self.maNVInput.setStyleSheet("""
                background-color: #ccc;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                color: #333;""")
        self.maNVInput.setGeometry(26, 72, 300, 35)
        self.maNVInput.setReadOnly(True)

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

        self.faceButton = QPushButton("Chọn ảnh", StaffAddPanel)
        self.faceButton.setGeometry(432, 270, 101, 33)
        self.faceButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: #9F9B9B;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #CDCDCD;}"
                                        "QPushButton:pressed {background-color: darkgray;}")
        self.pixmap = QPixmap()
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

        # Đăng ksi khuôn mặt
        faceLabel = QLabel("Đăng kí khuôn mặt", StaffAddPanel)
        faceLabel.setStyleSheet("font-size: 16pt;")
        faceLabel.setGeometry(26, 512, 200, 30)

        self.faceButton = QPushButton("Chụp hình", StaffAddPanel)
        self.faceButton.setGeometry(210, 517, 75, 23)
        self.faceButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: #9F9B9B;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #CDCDCD;}"
                                        "QPushButton:pressed {background-color: darkgray;}")

        signedLabel = QLabel("*Chưa đăng kí", StaffAddPanel)
        signedLabel.setStyleSheet("font-size: 12pt;color: #FF0000")
        signedLabel.setGeometry(26, 541, 220, 22)

        self.faceButton.clicked.connect(self.showFaceRecognition)

        # Hủy
        self.cancelButton = QPushButton("Hủy", StaffAddPanel)
        self.cancelButton.setGeometry(112, 600, 125, 50)
        self.cancelButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        self.cancelButton.clicked.connect(self.close) 
        
        # Cập nhật
        self.updateButton = QPushButton("Lưu", StaffAddPanel)
        self.updateButton.setGeometry(389, 600, 125, 50)
        self.updateButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        self.updateButton.clicked.connect(self.updateDB)


    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Chọn Ảnh", "", "Image Files (*.png *.jpg *.bmp *.jpeg)")
        
        if file_path:
            self.pixmap = QPixmap(file_path)  # Tải hình ảnh từ đường dẫn tệp được chọn
            scaled_pixmap = self.pixmap.scaled(self.avataLabel.size(), aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio)  # Thay đổi kích thước ảnh nếu cần
            self.avataLabel.setPixmap(scaled_pixmap)  # Đặt hình ảnh vào QLabel
            self.avataLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            #  Check if image is valid
        # if file_path:
        #     # Use QImageReader to read image from file
        #     image_reader = QImageReader(file_path)
        #     image_reader.setAutoTransform(True)  # Enable automatic transformation based on image metadata
        #     image = image_reader.read()  # Read the image
            
        #     if not image.isNull():
        #         # Convert QImage to QPixmap
        #         pixmap = QPixmap.fromImage(image)
                
        #         # Scale pixmap while maintaining aspect ratio
        #         scaled_pixmap = pixmap.scaled(self.avataLabel.size(), aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio)
                
        #         # Set pixmap to QLabel
        #         self.avataLabel.setPixmap(scaled_pixmap)
        #         self.avataLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #     else:
        #         print("Error: Failed to load image.")

    def showFaceRecognition(self):
        self.faceRecognitionWidget = FaceRecognitionWidget.FaceRecognitionWidget()  
        id = self.maNVInput.text()
        name = self.tenNVInput.text()
        self.faceRecognitionWidget.faceDetect(id,name)
        self.faceRecognitionWidget.close()

    def list_CV(self):
        # Kết nối đến cơ sở dữ liệu và nhận đối tượng cursor
        db_connector = DBConnect()
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
        db_connector =DBConnect()
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

    def selected_data(self, data):
        db_connector = DBConnect()
        mycursor = db_connector.connect()

        # Kiểm tra nếu kết nối thành công
        if mycursor is not None:
            # Thực hiện truy vấn
            sql = "SELECT maNV, tenNV, sDT, ngaySinh, gioiTinh, tenPB, tenCV, Luong, hinhanh FROM staff INNER JOIN department ON staff.maPB = department.maPB inner join position as pos on staff.maCV = pos.maCV where maNV = %s"
            mycursor.execute(sql,(data,))
            # Lấy kết quả
            results  = mycursor.fetchall()
            for record in results:
                maNV, tenNV, sDT, ngaySinh, gioiTinh, tenPB, tenCV, luong, hinhanh = record
                staff = Staff(maNV, tenNV, sDT, ngaySinh, gioiTinh, tenPB, tenCV, luong, hinhanh)
                self.staff_list.append(staff)
            # Đóng kết nối sau khi hoàn thành

            self.maNVInput.setText(str(staff.getMaNV()))
            self.tenNVInput.setText(staff.getTenNV())
            self.sDTInput.setText(staff.getSDT())
            self.ngaySinhInput.setDate(staff.getNgaySinh())
            for index in range(self.viTriComboBox.count()):
                if self.viTriComboBox.itemText(index) == tenPB:
                    self.viTriComboBox.setCurrentIndex(index)
                    break  # Stop searching once found
            if staff.getGioiTinh() == 0:
                self.namCB.setChecked(True)
            else: 
                self.nuCB.setChecked(True)
           # Find the index of the job position by name and set it
            for index in range(self.chucVuComboBox.count()):
                if self.chucVuComboBox.itemText(index) == tenCV:
                    self.chucVuComboBox.setCurrentIndex(index)
                    break  # Stop searching once found
            self.luongInput.setText(str(staff.getLuong()))

            # self.avataLabel.loadFromData(hinhanh)
            # Create QPixmap from image data
            print("===============================================")
            try:
                self.pixmap.loadFromData(hinhanh)
                if self.pixmap.isNull():
                    print("Failed to load image: QPixmap is null")
                scaled_pixmap = self.pixmap.scaled(self.avataLabel.size(), aspectRatioMode=Qt.AspectRatioMode.IgnoreAspectRatio)
                self.avataLabel.setPixmap(scaled_pixmap)
                self.avataLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
            except Exception as e:
                print(f"Error loading image: {e}")
            print("===============================================")

            db_connector.close()
        else:
            print("Failed to connect to database")

    def updateDB(self):
        maNV = self.maNVInput.text()
        tenNV = self.tenNVInput.text()
        sDT = self.sDTInput.text()
        ngaySinh = self.ngaySinhInput.date().toString(Qt.DateFormat.ISODate)
        for PB in self.PB_list:
            if PB.getTenPB() == self.viTriComboBox.currentText():
                maPB = PB.getMaPB()
        if self.namCB.isChecked():
            gioiTinh = 0
        else: 
            gioiTinh = 1
        for CV in self.CV_list:
            if CV.getTenCV() == self.chucVuComboBox.currentText():
                maCV = CV.getMaCV()
        luong = self.luongInput.text()


        # Chuyển đổi QPixmap thành QImage
        image = self.pixmap.toImage()

        # Chuyển đổi QImage thành dữ liệu bytes
        image_data = QByteArray()
        buffer = QBuffer(image_data)
        buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        image.save(buffer, "jpg")
        try:
            self.staff_dao = StaffDAO()
            self.staff_dao.update(maNV, tenNV, sDT, ngaySinh, gioiTinh, maPB,maCV,luong,image_data)
            QMessageBox.information(self, "Thông báo", "Bạn đã sửa thông tin nhân viên thành công!")

            # trả lại giá trị mặc định
            self.viTriComboBox.clear()
            self.chucVuComboBox.clear()
            self.PB_list.clear()
            self.staff_list.clear()
            self.close()
        except:
            QMessageBox.information(self, "Thông báo", "Ảnh (Phiên bản ICC không được hỗ trợ)")

    def checkDKKM(self):
        # global signedLabel
        manv = self.maNVInput.text()
        with open('plugin/ID.txt', 'r',encoding='utf-8') as file:
            for line in file:
                if manv == line.split(' - ')[0].strip():
                    signedLabel.setText("*Đã đăng kí")
                    signedLabel.setStyleSheet("font-size: 12pt;color: #008F06")


    def closeEvent(self, event):
        # Gọi hàm để thực hiện các thao tác sau khi cửa sổ được đóng
        self.on_window_close()

    def on_window_close(self):
        # Thực hiện các thao tác sau khi cửa sổ được đóng
        self.chucVuComboBox.clear()
        self.viTriComboBox.clear()
        self.PB_list.clear()
        self.CV_list.clear()

    def showCancelButton(self):
        self.cancelButton.show()

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
