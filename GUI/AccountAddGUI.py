from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QApplication, QLineEdit,QCheckBox,QComboBox,QCalendarWidget,QDateEdit,QToolButton,QMessageBox
from PyQt6.QtCore import Qt,QDate

from DAO.AccountDAO import  AccountDAO
from DAO import DBConnect
from DTO import Account,Staff

class AccountAddGUI(QWidget):
    # PB_list = []
    # CV_list = []
    account_list = []
    staff_list = []
    phanquyen_list = ['Admin', 'Nhân viên', 'Quản lý', 'Chủ doanh nghiệp']

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a login panel widget
        self.setFixedSize(634, 720)

        AccountAddPanel = QWidget(self)  # Specify parent widget
        AccountAddPanel.setStyleSheet("background-color: #B8B8B8;")
        AccountAddPanel.setFixedSize(634, 720)

        # mã nhân viên
        self.list_NV()
        maNVLabel = QLabel("Mã nhân viên", AccountAddPanel)
        maNVLabel.setStyleSheet("font-size: 16pt;")
        maNVLabel.setGeometry(26, 31, 291, 30)
        
        self.NhanVienComboBox = QComboBox(AccountAddPanel)  # Change to QComboBox
        self.NhanVienComboBox.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.NhanVienComboBox.setGeometry(26, 72, 300, 35)
        for nhanvien in self.staff_list:
            self.NhanVienComboBox.addItem(str(nhanvien.getMaNV()))
        self.NhanVienComboBox.currentIndexChanged.connect(self.updateTenNV)
        
        # tên nhân viên
        tenNVLabel = QLabel("Tên nhân viên", AccountAddPanel)
        tenNVLabel.setStyleSheet("font-size: 16pt;")
        tenNVLabel.setGeometry(26, 130, 291, 30)

        self.tenNVInput = QLineEdit(AccountAddPanel)
        self.tenNVInput.setStyleSheet("""
                background-color: #ccc;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                color: #333;""")
        self.tenNVInput.setGeometry(26, 171, 300, 35)
        self.tenNVInput.setReadOnly(True)

        # mật khẩu
        MKLabel = QLabel("Mật khẩu", AccountAddPanel)
        MKLabel.setStyleSheet("font-size: 16pt;")
        MKLabel.setGeometry(26, 328, 291, 30)

        self.MKInput = QLineEdit(AccountAddPanel)
        self.MKInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.MKInput.setGeometry(26, 369, 300, 35)

        # phân quyền
        PQLabel = QLabel("Phân quyền", AccountAddPanel)
        PQLabel.setStyleSheet("font-size: 16pt;")
        PQLabel.setGeometry(26, 229, 291, 30)

        self.phanQuyenComboBox = QComboBox(AccountAddPanel)
        self.phanQuyenComboBox.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.phanQuyenComboBox.setGeometry(26, 270, 300, 35)
        for phanquyen in self.phanquyen_list:
            self.phanQuyenComboBox.addItem(phanquyen)
        self.phanQuyenComboBox.setCurrentIndex(-1)

        # Thêm
        self.addButton = QPushButton("Thêm", AccountAddPanel)
        self.addButton.setGeometry(250, 600, 125, 50)
        self.addButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        
        self.addButton.clicked.connect(self.addPB)
    

    def addPB(self):
        maNV = self.NhanVienComboBox.currentText()
        for staff in self.staff_list:
            if staff.getMaNV() == maNV:
                maNV = staff.getMaNV()
                break
        matkhau = self.MKInput.text()
        phanquyen = self.phanQuyenComboBox.currentText()
        self.acc_dao = AccountDAO()
        self.acc_dao.add(maNV, matkhau, phanquyen)
    
    def list_NV(self):
        # Kết nối đến cơ sở dữ liệu và nhận đối tượng cursor
        db_connector = DBConnect.DBConnect()
        mycursor = db_connector.connect()

        # Kiểm tra nếu kết nối thành công
        if mycursor is not None:
            # Thực hiện truy vấn
            sql = "SELECT maNV, tenNV, sdt, ngaySinh, gioiTinh, maPB, maCV, luong from staff where not exists (select 1 from account where staff.maNV = account.maNV)"
            mycursor.execute(sql)
            # Lấy kết quả
            results  = mycursor.fetchall()

            for record in results:
                maNV, tenNV, sdt, ngaySinh, gioiTinh, maPB, maCV, luong = record
                staff = Staff.Staff(maNV, tenNV, sdt, ngaySinh, gioiTinh, maPB, maCV, luong)
                self.staff_list.append(staff)
                print(staff.getTenNV())
            # Đóng kết nối sau khi hoàn thành
            db_connector.close()
        else:
            print("Failed to connect to database")
    
    def updateTenNV(self):
        # Lấy chỉ mục hiện tại được chọn từ combobox
        index = self.NhanVienComboBox.currentIndex()

        # Nếu chỉ mục hiện tại hợp lệ (không phải -1)
        if index != -1:
            # Lấy đối tượng Staff tương ứng với chỉ mục hiện tại
            staff = self.staff_list[index]
            # Lấy tên nhân viên từ đối tượng Staff
            tenNV = staff.getTenNV()
            self.tenNVInput.setText(tenNV)
        else:
            self.tenNVInput.setText("")
            
            
    def closeEvent(self, event):
        # Gọi hàm để thực hiện các thao tác sau khi cửa sổ được đóng
        self.on_window_close()

    def on_window_close(self):
        # Thực hiện các thao tác sau khi cửa sổ được đóng
        self.NhanVienComboBox.clear()
        self.staff_list.clear()
