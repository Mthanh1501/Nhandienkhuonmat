import cv2
import numpy as np
from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap

from datetime import datetime

from PyQt6.QtWidgets import QAbstractItemView,QTableView,QHeaderView,QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from GUI import FaceRecognitionThread

from DAO import CheckInDAO,CheckOutDAO

class CheckInGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.face_recognition_thread = None
        # self.current_name = "Unknown"
        # self.current_id = "Unknown"
        self.initUI()
        
        
    def initUI(self):
        # Cài đặt các thành phần giao diện người dùng
        self.setFixedSize(897, 656)
        self.cameraLabel = QLabel(self)
        self.cameraLabel.setGeometry(0, 0, 480, 360)

        NVlabel = QLabel(self)
        NVlabel.setGeometry(482, 0, 415, 360)

        maNVLabel = QLabel("Mã nhân viên", NVlabel)
        maNVLabel.setStyleSheet("font-size: 16pt;")
        maNVLabel.setGeometry(18, 45, 190, 30)

        self.maNVInput = QLabel("",NVlabel)
        self.maNVInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.maNVInput.setGeometry(18, 112, 190, 30)

        # tên nhân viên
        tenNVLabel = QLabel("Tên nhân viên", NVlabel)
        tenNVLabel.setStyleSheet("font-size: 16pt;")
        tenNVLabel.setGeometry(18, 180, 190, 30)

        self.tenNVInput = QLabel("",NVlabel)
        self.tenNVInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.tenNVInput.setGeometry(18, 247, 190, 30)

        self.CheckIN = QPushButton("Vào ca", NVlabel)
        self.CheckIN.setGeometry(63, 314, 108, 29)
        self.CheckIN.setStyleSheet("QPushButton {border-radius: 5px;background-color: #9F9B9B;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #CDCDCD;}"
                                        "QPushButton:pressed {background-color: darkgray;}")
        
        self.CheckIN.clicked.connect(self.checkIn)

        self.CheckOut = QPushButton("Ra ca", NVlabel)
        self.CheckOut.setGeometry(252, 314, 108, 29)
        self.CheckOut.setStyleSheet("QPushButton {border-radius: 5px;background-color: #9F9B9B;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #CDCDCD;}"
                                        "QPushButton:pressed {background-color: darkgray;}")
        
        self.CheckOut.clicked.connect(self.checkOut)
        

        self.tableWidget = QTableView(self)
        self.tableWidget.setGeometry(5, 367, 887, 291)
        self.model = QStandardItemModel(self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Đặt mô hình cho TableView
        self.tableWidget.setModel(self.model) # chỉ chọn hàng
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # tắt cột số
        
        self.tableWidget.verticalHeader().setVisible(False)# Đặt font in đậm cho tiêu đề ngang
        header_font = self.tableWidget.horizontalHeader().font()
        header_font.setBold(True)
        self.tableWidget.horizontalHeader().setFont(header_font) # tắt thanh cuộn
        self.tableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)# không cho sửa
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # Không cho phép chỉnh sửa ô
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)  # Chỉnh sửa chế độ thay đổi kích thước cột

        # Đặt nội dung cho tiêu đề ngang        
        headers = ["Mã nhân viên", "Tên nhân viên", "Thời gian"]
        self.model.setHorizontalHeaderLabels(headers)
        # Set model cho TableView
        self.tableWidget.setStyleSheet("background-color: white;")

        self.face_recognition_thread = None


        self.startFaceRecognitionThread()

        # Sử dụng QTimer để cập nhật giao diện định kỳ
        self.timer = QTimer(self)
       
        self.timer.timeout.connect(self.update_image)

        self.timer.start(30)  # Cập nhật hình ảnh mỗi 30 ms

    def startFaceRecognitionThread(self):
        if self.face_recognition_thread is not None:
            self.face_recognition_thread.stop()
            self.face_recognition_thread.wait()
        self.face_recognition_thread = FaceRecognitionThread.FaceRecognitionThread()
        self.face_recognition_thread.face_detected.connect(self.update_gui)
        self.face_recognition_thread.start()

    def closeEvent(self, event):
        self.face_recognition_thread.stop()
        super().closeEvent(event)

    def checkIn(self):
        maNV =self.maNVInput.text()
        tenNV = self.tenNVInput.text()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.checkIn_dao = CheckInDAO.CheckInDAO()
        self.checkIn_dao.add(maNV,current_time)


        id_item = QStandardItem(maNV)
        name_item = QStandardItem(tenNV)
        current_time_item = QStandardItem(current_time)

        items = [id_item, name_item,current_time_item]
        self.model.appendRow(items)

        # Scroll đến cuối cùng của bảng
        last_row_index = self.model.rowCount() - 1
        last_index = self.model.index(last_row_index, 0)
        self.tableWidget.scrollTo(last_index)

        # Đảm bảo bảng đang hiển thị ở dòng cuối cùng
        self.tableWidget.setCurrentIndex(last_index)
        # Set model cho TableView
        self.tableWidget.setStyleSheet("background-color: white;")

    def checkOut(self):
        maNV =self.maNVInput.text()
        tenNV = self.tenNVInput.text()
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time_today = datetime.now().strftime('%Y-%m-%d')

        self.checkOut_dao = CheckOutDAO.CheckOutDAO()
        self.checkOut_dao.add(maNV,current_time,time_today)


        id_item = QStandardItem(maNV)
        name_item = QStandardItem(tenNV)
        current_time_item = QStandardItem(current_time)

        items = [id_item, name_item,current_time_item]
        self.model.appendRow(items)

        # Scroll đến cuối cùng của bảng
        last_row_index = self.model.rowCount() - 1
        last_index = self.model.index(last_row_index, 0)
        self.tableWidget.scrollTo(last_index)

        # Đảm bảo bảng đang hiển thị ở dòng cuối cùng
        self.tableWidget.setCurrentIndex(last_index)
        # Set model cho TableView
        self.tableWidget.setStyleSheet("background-color: white;")


    def update_gui(self, name, id):
        self.maNVInput.setText(id)
        self.tenNVInput.setText(name)

    def update_image(self):
        # Cập nhật hình ảnh trên QLabel từ camera
        ret, img = self.face_recognition_thread.cam.read()
        if ret:
            try:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                resized_img = cv2.resize(img_rgb, (480, 360))
                h, w, ch = resized_img.shape
                qimg = QImage(resized_img.data, w, h, w * ch, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(qimg)
                self.cameraLabel.setPixmap(pixmap)
            except Exception as e:
                print(f"Error updating image: {e}")
        # else:
        #     print("Error reading camera frame")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    gui = CheckInGUI()
    gui.show()
    sys.exit(app.exec())
