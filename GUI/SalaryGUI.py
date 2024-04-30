
from PyQt6.QtWidgets import QWidget, QLineEdit, QAbstractItemView,QTableView,QHeaderView,QPushButton, QComboBox, QLabel
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, pyqtSignal,QDate,QTime
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from datetime import datetime

from DTO.Staff import Staff
from DTO.Position import Position
from DTO.Checkin import Checkin
from DTO.Checkout import Checkout
from DAO.DBConnect import DBConnect
from DAO.SalaryDAO import  SalaryDAO
import copy

from GUI import SalaryDetailGUI

class SalaryGUI(QWidget):    
    # staff_list = []
    salary_list = []
    years_list = []
    months = []

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # Create a home panel widget
        self.setFixedSize(897, 656)

        salarypanel = QWidget(self)  # Specify parent widget
        salarypanel.setStyleSheet("background-color: #CDCDCD;")
        salarypanel.move(0, 0)
        salarypanel.setFixedSize(897, 656)

        # Xem
        self.detailButton = QPushButton("Xem", salarypanel)
        self.detailButton.setGeometry(35, 19, 125, 50)
        self.detailButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        self.detailButton.clicked.connect(self.showSalaryDetail)     
        
        # nút chọn tìm kiếm bảng lương theo tháng hoặc theo năm
        yearLabel = QLabel("Năm", salarypanel)
        yearLabel.setStyleSheet("font-size: 10pt;")
        yearLabel.setGeometry(180, 10, 291, 30)
        
        self.years_list = self.getYear()
        self.yearComboBox = QComboBox(self)
        self.yearComboBox.setGeometry(180, 35, 100, 30)
        self.yearComboBox.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        for year in self.years_list:
            self.yearComboBox.addItem(year)
        self.yearComboBox.setCurrentIndex(-1)
        self.yearComboBox.currentIndexChanged.connect(self.updateMonthComboBox)

        monthLabel = QLabel("Tháng", salarypanel)
        monthLabel.setStyleSheet("font-size: 10pt;")
        monthLabel.setGeometry(300, 10, 291, 30)
        self.monthComboBox = QComboBox(self)
        self.monthComboBox.setGeometry(300, 35, 100, 30)
        self.monthComboBox.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        
        # nút lọc
        self.filterButton = QPushButton("Lọc", salarypanel)
        self.filterButton.setGeometry(415, 35, 50, 30)
        self.filterButton.clicked.connect(self.filterDate)

        # tìm kiếm
        self.searchInput = QLineEdit(salarypanel)
        self.searchInput.setPlaceholderText("Tìm kiếm theo Mã hoặc Tên Nhân viên....")
        self.searchInput.setStyleSheet("""
                color: rgba(0, 0, 0, 0.5);
                background-color:White;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                padding-left: 17px """)
        self.searchInput.returnPressed.connect(self.search)
        def clearPlaceholderText():
            if self.searchInput.text() == "Tìm kiếm theo Mã hoặc Tên Nhân viên....":
                self.searchInput.clear()
                
        def restorePlaceholderText():
            if self.searchInput.text() == "":
                self.searchInput.setPlaceholderText("Tìm kiếm theo Mã hoặc Tên Nhân viên....")

        self.searchInput.textChanged.connect(restorePlaceholderText)
        self.searchInput.editingFinished.connect(clearPlaceholderText)
        self.searchInput.setGeometry(572, 19, 288, 50)
        


        # tạo bảng
        self.tableWidget = QTableView(salarypanel)
        self.tableWidget.setGeometry(9, 95, 869, 432)
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
        headers = ["Mã nhân viên", "Tên nhân viên", "Chức vụ", "Lương/giờ", "Ngày", "Tổng tiền (VND)"]

        self.model.setHorizontalHeaderLabels(headers)
        # Thêm dữ liệu vào bảng 
        self.load_data_staff()
        self.show_data_staff()


    def load_data_staff(self):
        self.salary_list.clear()
        # Kết nối đến cơ sở dữ liệu và nhận đối tượng cursor
        db_connector = DBConnect()
        mycursor = db_connector.connect()

        # Kiểm tra nếu kết nối thành công
        if mycursor is not None:
            # Thực hiện truy vấn
            # sql = "SELECT staff.maNV, staff.tenNV, position.tenCV, checkin.ngayVao, checkin.gioVao, checkout.gioRa, staff.Luong \
            #        FROM staff inner join position on staff.maCV = position.maCV inner join checkin on staff.maNV = checkin.maNV inner join checkout on staff.maNV = checkout.maNV \
            #        WHERE staff.trangthai = 1 \
            #        ORDER BY staff.maNV asc"
            sql = "SELECT staff.maNV, staff.tenNV, position.tenCV, chamcong.vaoCa, chamcong.raCa, staff.Luong  \
                   FROM staff inner join position on staff.maCV = position.maCV inner join chamcong on staff.maNV = chamcong.maNV \
                   WHERE staff.trangthai = 1 \
                   ORDER BY staff.maNV asc"
            mycursor.execute(sql)
            # Lấy kết quả
            results  = mycursor.fetchall()

            for record in results:
                
                # maNV, tenNV, tenCV, ngayVao, gioVao, gioRa, Luong = record
                maNV, tenNV, tenCV, vaoCa, raCa, Luong = record
                
                if vaoCa is not None and raCa is not None:
                    to_str_giovao = str(vaoCa)
                    to_str_giora = str(raCa)
                    
                    datetime_vaoCa = datetime.strptime(to_str_giovao, '%Y-%m-%d %H:%M:%S')
                    datetime_raCa = datetime.strptime(to_str_giora, '%Y-%m-%d %H:%M:%S')
                
                    timein = QTime(datetime_vaoCa.hour, datetime_vaoCa.minute, datetime_vaoCa.second)
                    timeout = QTime(datetime_raCa.hour, datetime_raCa.minute, datetime_raCa.second)
                    ngayVao = datetime_vaoCa.date()
                    
                    tongGio = timein.secsTo(timeout) / 3600
                    
                    tongTien = round((tongGio * Luong), 2)
                    
                    # self.salary_list.append((maNV, tenNV, tenCV, ngayVao, Luong, tongTien))
                    try:
                        mycursor = db_connector.connect()
                        check_query = "SELECT * FROM salary WHERE maNV = %s AND ngay = %s"
                        check_values = (maNV, ngayVao)
                        mycursor.execute(check_query, check_values)
                        existing_record = mycursor.fetchone()
                        
                        if not existing_record:
                            query = "INSERT INTO `salary`(`maNV`, `ngay`, `thoigianlam`, `tongtien`) VALUES (%s,%s,%s,%s)"
                            
                            values = (maNV, ngayVao, tongGio, tongTien)
                            mycursor.execute(query, values)
                            db_connector.connection.commit()
                    finally:
                        db_connector.close()
                    # self.salary_list.append((maNV, tenNV, tenCV, ngayVao, Luong, tongTien))
                else:
                    pass
            try:
                mycursor = db_connector.connect()
                sql = "SELECT staff.maNV, staff.tenNV, position.tenCV, salary.ngay, staff.Luong, salary.tongTien  \
                    FROM staff inner join position on staff.maCV = position.maCV inner join salary on staff.maNV = salary.maNV \
                    WHERE staff.trangthai = 1 \
                    ORDER BY staff.maNV asc"
                mycursor.execute(sql)
                # Lấy kết quả
                results  = mycursor.fetchall()
                for record in results:
                    maNV, tenNV, tenCV, ngay, luong, tongTien = record
                    self.salary_list.append((maNV, tenNV, tenCV, ngay, luong, tongTien))
            finally:
                db_connector.close()    
            
            # Đóng kết nối sau khi hoàn thành
            db_connector.close()
        else:
            print("Failed to connect to database")

    def show_data_staff(self):
    # Khởi tạo model và đặt tiêu đề
        self.model.removeRows(0, self.model.rowCount())
        headers = ["Mã nhân viên", "Tên nhân viên", "Chức vụ", "Ngày", "Lương/giờ", "Tổng tiền (VND)"]
        self.model.setHorizontalHeaderLabels(headers)
    
        # Thêm dữ liệu từ danh sách staff_list vào model
        for salary in self.salary_list:
            row = list(salary)
            # Tạo một danh sách các Item dựa trên dữ liệu của staff
            items = [QStandardItem(str(item)) for item in row]
            # Thêm hàng vào model
            self.model.appendRow(items)

        # Set model cho TableView
        self.tableWidget.setStyleSheet("background-color: white;")

    def showSalaryDetail(self):
        # Lấy chỉ mục hàng hiện tại từ bảng
        current_index = self.tableWidget.currentIndex()
        # Kiểm tra xem chỉ mục có hợp lệ không
        if current_index.isValid():
            # Lấy chỉ mục hàng và cột
            row = current_index.row()

            # Lấy dữ liệu từ mô hình tại chỉ mục hàng và cột
            item = self.model.item(row)
            if item is not None:
                data = item.text()
                print(data)
                self.salaryDetail = SalaryDetailGUI.SalaryDetailGUI()
                self.salaryDetail.selected_data(data)
                self.salaryDetail.show()  # Truyền tham chiếu của nút "Xem"       
        else:
            print("No valid index selected")
            
    def getYear(self):
        db_connector = DBConnect()
        mycursor = db_connector.connect()
        sql = "SELECT DISTINCT YEAR(ngay) FROM salary"
        mycursor.execute(sql)
            # Lấy kết quả
        results  = mycursor.fetchall()
        
        years = [str(row[0]) for row in results]
        
        db_connector.close() 
        
        return years

    
    def updateMonthComboBox(self, index):
        if index == -1:
            return

        selected_year = int(self.yearComboBox.currentText())

        # Mocking database query to get months for the selected year
        # In a real application, replace this with your database query
        current_year = datetime.now().year
        current_month = datetime.now().month
        if selected_year < current_year:
            months = list(range(1, 13))
        elif selected_year == current_year:
            months = list(range(1, current_month + 1))
        else:
            months = []

        self.monthComboBox.clear()
        self.monthComboBox.addItems([str(month) for month in months])
        
    def filterDate(self):
        db_connector = DBConnect()
        mycursor = db_connector.connect()
        
        year = self.yearComboBox.currentText()
        month = self.monthComboBox.currentText()
        
        if not year and not month:
            sql = "SELECT staff.maNV, staff.tenNV, position.tenCV, salary.ngay, staff.Luong, salary.tongTien  \
                    FROM staff inner join position on staff.maCV = position.maCV inner join salary on staff.maNV = salary.maNV \
                    WHERE staff.trangthai = 1 \
                    ORDER BY staff.maNV asc"
            mycursor.execute(sql)
        else:
            if mycursor is not None:
                sql = "SELECT staff.maNV, staff.tenNV, position.tenCV, salary.ngay, staff.Luong, salary.tongTien  \
                       FROM staff inner join position on staff.maCV = position.maCV inner join salary on staff.maNV = salary.maNV \
                       WHERE YEAR(ngay) = %s and MONTH(ngay) = %s"
                mycursor.execute(sql, (year,month))
        results = mycursor.fetchall()
        self.salary_list.clear()
        for record in results:
            maNV, tenNV, tenCV, ngay, luong, tongTien = record
            self.salary_list.append((maNV, tenNV, tenCV, ngay, luong, tongTien))
        
        # Hiển thị dữ liệu tìm kiếm lên bảng
        self.show_data_staff()
        
        # Đóng kết nối
        db_connector.close()   
    
    def search(self):
        db_connector = DBConnect()
        mycursor = db_connector.connect()
        
        search_text = self.searchInput.text()
        if not search_text:
            sql = "SELECT staff.maNV, staff.tenNV, position.tenCV, salary.ngay, staff.Luong, salary.tongTien  \
                    FROM staff inner join position on staff.maCV = position.maCV inner join salary on staff.maNV = salary.maNV \
                    WHERE staff.trangthai = 1 \
                    ORDER BY staff.maNV asc"
            
            mycursor.execute(sql)
        else:
            if mycursor is not None:
                sql = "SELECT staff.maNV, staff.tenNV, position.tenCV, salary.ngay, staff.Luong, salary.tongTien  \
                       FROM staff inner join position on staff.maCV = position.maCV inner join salary on staff.maNV = salary.maNV \
                       WHERE staff.trangthai = 1 and (salary.maNV LIKE %s or tenNV LIKE %s)"
                mycursor.execute(sql, ('%' + search_text + '%', '%' + search_text + '%'))
        
        results = mycursor.fetchall()
        self.salary_list.clear()
        for record in results:
            maNV, tenNV, tenCV, ngay, luong, tongTien = record
            self.salary_list.append((maNV, tenNV, tenCV, ngay, luong, tongTien))
        
        # Hiển thị dữ liệu tìm kiếm lên bảng
        self.show_data_staff()
        
        # Đóng kết nối
        db_connector.close()
        
    def reload(self):
        self.load_data_staff()
        self.show_data_staff()
        self.years.clear()
        self.months.clear()
        
