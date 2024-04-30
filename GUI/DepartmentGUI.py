
from PyQt6.QtWidgets import QWidget, QLineEdit, QAbstractItemView,QTableView,QHeaderView,QPushButton
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from DTO.Department import Department
from DAO.DepartmentDAO import  DepartmentDAO
from DAO.DBConnect import DBConnect

from GUI import DepartmentAddGUI, DepartmentDetailGUI

class DepartmentGUI(QWidget):    
    # staff_list = []
    department_list = []

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        # Create a home panel widget
        self.setFixedSize(897, 656)

        dpmpanel = QWidget(self)  # Specify parent widget
        dpmpanel.setStyleSheet("background-color: #CDCDCD;")
        dpmpanel.move(0, 0)
        dpmpanel.setFixedSize(897, 656)

        # Thêm
        self.addButton = QPushButton("Thêm", dpmpanel)
        self.addButton.setGeometry(35, 19, 125, 50)
        self.addButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        self.addButton.clicked.connect(self.showDepartmentAdd)   

        # Xem
        self.detailButton = QPushButton("Xem", dpmpanel)
        self.detailButton.setGeometry(213, 19, 125, 50)
        self.detailButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        self.detailButton.clicked.connect(self.showDepartmentDetail)     

        # Xóa
        self.deleteButton = QPushButton("Xóa", dpmpanel)
        self.deleteButton.setGeometry(388, 19, 125, 50)
        self.deleteButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        self.deleteButton.clicked.connect(self.deleteDPM)

        # tìm kiếm
        self.searchInput = QLineEdit(dpmpanel)
        self.searchInput.setPlaceholderText("Tìm kiếm theo ID, Tên hoặc Địa điểm PB....")
        self.searchInput.setStyleSheet("""
                color: rgba(0, 0, 0, 0.5);
                background-color:White;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                padding-left: 17px """)
        self.searchInput.returnPressed.connect(self.search)
        
        def clearPlaceholderText():
            if self.searchInput.text() == "Tìm kiếm theo ID, Tên hoặc Địa điểm PB....":
                self.searchInput.clear()
                
        def restorePlaceholderText():
            if self.searchInput.text() == "":
                self.searchInput.setPlaceholderText("Tìm kiếm theo ID, Tên hoặc Địa điểm PB....")

        self.searchInput.textChanged.connect(restorePlaceholderText)
        self.searchInput.editingFinished.connect(clearPlaceholderText)
        self.searchInput.setGeometry(572, 19, 288, 50)


        # tạo bảng
        self.tableWidget = QTableView(dpmpanel)
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
        headers = ["Mã phòng ban", "Tên phòng ban", "Địa điểm phòng ban"]

        self.model.setHorizontalHeaderLabels(headers)
        # Thêm dữ liệu vào bảng 
        self.load_data_staff()
        self.show_data_staff()


    def load_data_staff(self):
        self.department_list.clear()
        # Kết nối đến cơ sở dữ liệu và nhận đối tượng cursor
        db_connector = DBConnect()
        mycursor = db_connector.connect()

        # Kiểm tra nếu kết nối thành công
        if mycursor is not None:
            # Thực hiện truy vấn
            sql = "SELECT * FROM department order by maPB asc"
            mycursor.execute(sql)
            # Lấy kết quả
            results  = mycursor.fetchall()

            for record in results:
                maPB, tenPB, diaDiem = record
                department = Department(maPB, tenPB, diaDiem)
                self.department_list.append(department)
            # Đóng kết nối sau khi hoàn thành
            db_connector.close()
        else:
            print("Failed to connect to database")

    def show_data_staff(self):
    # Khởi tạo model và đặt tiêu đề
        self.model.removeRows(0, self.model.rowCount())
        headers = ["Mã phòng ban", "Tên phòng ban", "Địa điểm phòng ban"]
        self.model.setHorizontalHeaderLabels(headers)
    
        # Thêm dữ liệu từ danh sách staff_list vào model
        for dpm in self.department_list:
            row = [dpm.getMaPB(), dpm.getTenPB(), dpm.getDiaDiemPB()]
            # Tạo một danh sách các Item dựa trên dữ liệu của staff
            items = [QStandardItem(str(item)) for item in row]
            # Thêm hàng vào model
            self.model.appendRow(items)

        # Set model cho TableView
        self.tableWidget.setStyleSheet("background-color: white;")

    def showDepartmentAdd(self):
        self.dpmAdd = DepartmentAddGUI.DepartmentAddGUI()
        self.dpmAdd.show()
        self.dpmAdd.addButton.clicked.connect(self.reload)

    def showDepartmentDetail(self):
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
                self.dpmDetail = DepartmentDetailGUI.DepartmentDetailGUI()
                self.dpmDetail.selected_data(data)
                self.dpmDetail.show()  # Truyền tham chiếu của nút "Xem"
            self.dpmDetail.updateButton.clicked.connect(self.reload)        
        else:
            QMessageBox.warning(None, "Nhắc nhở", 'Vui lòng click chọn phòng ban muốn xem thông tin chi tiết!')

    def deleteDPM(self):
        # Lấy chỉ mục hàng hiện tại từ bảng
        current_index = self.tableWidget.currentIndex()
        # Kiểm tra xem chỉ mục có hợp lệ không
        if current_index.isValid():
                        
            reply = QMessageBox.question(self, "Xác nhận xóa", 'Bạn có chắc chắn muốn xóa phòng ban này không?', QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)  
            
            if reply == QMessageBox.StandardButton.Yes:      
                #xác định chỉ mục của cột
                row = current_index.row()

                # Lấy dữ liệu từ mô hình tại chỉ mục hàng và cột
                item = self.model.item(row)
                if item is not None:
                    data = item.text()
                    self.dpm_dao = DepartmentDAO()
                    self.dpm_dao.delete(data)
                self.reload()      
        else:
            print("No valid index selected")
    
    def search(self):
        db_connector = DBConnect()
        mycursor = db_connector.connect()
        
        search_text = self.searchInput.text()
        if not search_text:
            sql = "SELECT * FROM department order by maPB asc"
            mycursor.execute(sql)
        else:
            if mycursor is not None:
                sql = "SELECT * FROM department WHERE maPB LIKE %s or tenPB LIKE %s or diadiem LIKE %s"
                mycursor.execute(sql, ('%' + search_text + '%', '%' + search_text + '%', '%' + search_text + '%'))
        
        results = mycursor.fetchall()
        self.department_list.clear()
        for record in results:
            maPB, tenPB, diadiem = record
            department = Department(maPB, tenPB, diadiem)
            self.department_list.append(department)
        
        # Hiển thị dữ liệu tìm kiếm lên bảng
        self.show_data_staff()
        
        # Đóng kết nối
        db_connector.close()
        
    def reload(self):
        self.load_data_staff()
        self.show_data_staff()