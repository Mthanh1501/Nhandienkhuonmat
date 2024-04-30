
from PyQt6.QtWidgets import QWidget, QLineEdit, QAbstractItemView,QTableView,QHeaderView,QPushButton
from PyQt6.QtWidgets import QApplication,QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from DTO.Staff import Staff
from DTO.Department import Department
from DTO.Position import Position
from GUI.StaffGUI import StaffGUI
from DAO.DBConnect import DBConnect

class StatisticsGUI(QWidget):    
    staff_list = []
    total_Staff = 0
    total_Department = 0
    total_Nghiviec = 0
    total_Account = 0

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # Create a home panel widget
        self.setFixedSize(897, 656)

        self.TKpanel = QWidget(self)  # Specify parent widget
        self.TKpanel.setStyleSheet("background-color: #CDCDCD;")
        self.TKpanel.move(0, 0)
        self.TKpanel.setFixedSize(897, 656)

        # Tổng nhân sự
        self.total_staff()
        total_staff_text = f"Tổng Nhân Sự: {self.total_Staff}"
        self.totalStaff = QLabel(total_staff_text, self.TKpanel)
        self.totalStaff.setGeometry(35, 19, 192, 82)
        self.totalStaff.setStyleSheet("""
            background-color: #117C47;
            border-radius: 3px;
            padding: 10px;
            font-weight: bold;
            color: white;
            font-size: 15px;
            """)
        
        # Tổng phòng ban
        self.total_department()
        total_department_text = f"Tổng Phòng Ban: {self.total_Department}"
        self.totalDepartment = QLabel(total_department_text, self.TKpanel)
        self.totalDepartment.setGeometry(247, 19, 192, 82)
        self.totalDepartment.setStyleSheet("""
            background-color: #E1AF04;
            border-radius: 3px;
            padding: 10px;
            font-weight: bold;
            color: white;
            font-size: 15px;
            """)

        # Tổng tài khoản người dùng
        self.total_account()
        total_account_text = f"Số tài khoản: {self.total_Account}"
        self.totalAccount = QLabel(total_account_text, self.TKpanel)
        self.totalAccount.setGeometry(459, 19, 192, 82)
        self.totalAccount.setStyleSheet("""
            background-color: #0000C9;
            border-radius: 3px;
            padding: 10px;
            font-weight: bold;
            color: white;
            font-size: 15px;
            """)
        
        # Tổng số nhân viên nghỉ việc
        self.total_nghiviec()
        total_nghiviec_text = f"Tổng NV thôi việc: {self.total_Nghiviec}"
        self.totalNghiviec = QLabel(total_nghiviec_text, self.TKpanel)
        self.totalNghiviec.setGeometry(671, 19, 192, 82)
        self.totalNghiviec.setStyleSheet("""
            background-color: #cb232a;
            border-radius: 3px;
            padding: 10px;
            font-weight: bold;
            color: white;
            font-size: 15px;
            """)
        

        # tạo bảng
        self.tableWidget = QTableView(self.TKpanel)
        self.tableWidget.setGeometry(13, 150, 869, 432)
        self.model = QStandardItemModel(self)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Thiết lập kích thước cố định cho các cột
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.tableWidget.setColumnWidth(0, 200)  # Thiết lập chiều rộng của cột thứ nhất
        self.tableWidget.setColumnWidth(1, 200)  # Thiết lập chiều rộng của cột thứ hai

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
        headers = ["STT", "Mã nhân viên", "Tên nhân viên", "Chức vụ", "Số điện thoại","Phòng Ban", "Lương/giờ"]

        self.model.setHorizontalHeaderLabels(headers)
        # Thêm dữ liệu vào bảng 
        self.load_data_staff()
        self.show_data_staff()


    def load_data_staff(self):
        # Kết nối đến cơ sở dữ liệu và nhận đối tượng cursor
        db_connector = DBConnect()
        mycursor = db_connector.connect()

        # Kiểm tra nếu kết nối thành công
        if mycursor is not None:
            # Thực hiện truy vấn
            sql = "SELECT staff.maNV, tenNV, pos.tenCV, sDT, tenPB, Luong \
                   FROM staff INNER JOIN department ON staff.maPB = department.maPB inner join position as pos on staff.maCV = pos.maCV \
                   WHERE staff.trangthai = 1 \
                   ORDER BY staff.maNV asc"
            mycursor.execute(sql)
            # Lấy kết quả
            results  = mycursor.fetchall()
            
            stt = 1; 

            for record in results:
                maNV, tenNV, tenCV, sDT, tenPB, Luong  = record
                self.staff_list.append((stt, maNV, tenNV, tenCV, sDT, tenPB, Luong))
                stt+=1
            # Đóng kết nối sau khi hoàn thành
            db_connector.close()
        else:
            print("Failed to connect to database")

    def show_data_staff(self):
    # Khởi tạo model và đặt tiêu đề
        self.model.removeRows(0, self.model.rowCount())
        headers = ["STT", "Mã nhân viên", "Tên nhân viên", "Chức vụ", "Số điện thoại","Phòng Ban", "Lương/giờ"]
        self.model.setHorizontalHeaderLabels(headers)
    
        # Thêm dữ liệu từ danh sách staff_list vào model
        for staff in self.staff_list:
            row = list(staff)
            # Tạo một danh sách các Item dựa trên dữ liệu của staff
            items = [QStandardItem(str(item)) for item in row]
            # Thêm hàng vào model
            self.model.appendRow(items)

        # Set model cho TableView
        self.tableWidget.setStyleSheet("background-color: white;")
        
    def total_staff(self):
        db_connector = DBConnect()
        mycursor = db_connector.connect()

        # Kiểm tra nếu kết nối thành công
        if mycursor is not None:
            # Thực hiện truy vấn để đếm số lượng nhân viên
            sql = "SELECT COUNT(*) FROM staff where trangthai = 1"
            mycursor.execute(sql)

            result = mycursor.fetchone()
            if result is not None:
                self.total_Staff = result[0]
                
    def total_department(self):
        db_connector = DBConnect()
        mycursor = db_connector.connect()

        # Kiểm tra nếu kết nối thành công
        if mycursor is not None:
            # Thực hiện truy vấn để đếm số lượng phòng ban
            sql = "SELECT COUNT(*) FROM department"
            mycursor.execute(sql)

            result = mycursor.fetchone()
            if result is not None:
                self.total_Department = result[0]
                
    def total_account(self):
        db_connector = DBConnect()
        mycursor = db_connector.connect()

        # Kiểm tra nếu kết nối thành công
        if mycursor is not None:
            # Thực hiện truy vấn để đếm số lượng tài khoản
            sql = "SELECT COUNT(*) FROM account inner join staff on account.maNV = staff.maNV where staff.trangthai = 1"
            mycursor.execute(sql)

            result = mycursor.fetchone()
            if result is not None:
                self.total_Account = result[0]     
        
    def total_nghiviec(self):
        db_connector = DBConnect()
        mycursor = db_connector.connect()

        # Kiểm tra nếu kết nối thành công
        if mycursor is not None:
            # Thực hiện truy vấn để đếm số lượng tài khoản
            sql = "SELECT COUNT(*) FROM staff where trangthai = 0"
            mycursor.execute(sql)

            result = mycursor.fetchone()
            if result is not None:
                self.total_Nghiviec = result[0]
                
    def reload(self):
        self.load_data_staff()
        self.show_data_staff()
        self.total_staff()
        self.total_department()
        self.total_account()
        self.total_nghiviec()
        
    def closeEvent(self, event):
        # Gọi hàm để thực hiện các thao tác sau khi cửa sổ được đóng
        self.on_window_close()

    def on_window_close(self):
        # Thực hiện các thao tác sau khi cửa sổ được đóng
        self.staff_list.clear()