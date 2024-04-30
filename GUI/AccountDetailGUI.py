from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit,QCheckBox,QComboBox,QCalendarWidget,QDateEdit,QMessageBox
from PyQt6.QtCore import Qt,QDate

from DAO.AccountDAO import  AccountDAO
from DAO.DBConnect import DBConnect
from DTO import Account

class AccountDetailGUI(QWidget):
    # staff_list = []
    # PB_list = []
    # CV_list = []
    
    account_list = []
    phanquyen_list = ['Admin', 'Nhân viên', 'Quản lý', 'Chủ doanh nghiệp']
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a login panel widget
        self.setFixedSize(634, 720)

        AccountDetailPanel = QWidget(self)  # Specify parent widget
        AccountDetailPanel.setStyleSheet("background-color: #B8B8B8;")
        AccountDetailPanel.setFixedSize(634, 720)

        # mã nhân viên
        maNVLabel = QLabel("Mã nhân viên", AccountDetailPanel)
        maNVLabel.setStyleSheet("font-size: 16pt;")
        maNVLabel.setGeometry(26, 31, 291, 30)

        self.maNVInput = QLineEdit(AccountDetailPanel)
        self.maNVInput.setStyleSheet("""
                background-color: #ccc;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                color: #333;""")
        self.maNVInput.setGeometry(26, 72, 300, 35)
        self.maNVInput.setReadOnly(True)
        
        # tên nhân viên
        tenNVLabel = QLabel("Tên nhân viên", AccountDetailPanel)
        tenNVLabel.setStyleSheet("font-size: 16pt;")
        tenNVLabel.setGeometry(26, 130, 291, 30)

        self.tenNVInput = QLineEdit(AccountDetailPanel)
        self.tenNVInput.setStyleSheet("""
                background-color: #ccc;
                border: 2px solid #B8B8B8;
                border-radius: 5px;
                color: #333;""")
        self.tenNVInput.setGeometry(26, 171, 300, 35)
        self.tenNVInput.setReadOnly(True)

        # mật khẩu
        MKLabel = QLabel("Mật khẩu", AccountDetailPanel)
        MKLabel.setStyleSheet("font-size: 16pt;")
        MKLabel.setGeometry(26, 328, 291, 30)

        self.MKInput = QLineEdit(AccountDetailPanel)
        self.MKInput.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.MKInput.setGeometry(26, 369, 300, 35)

        # Phân quyền
        PQLabel = QLabel("Phân quyền", AccountDetailPanel)
        PQLabel.setStyleSheet("font-size: 16pt;")
        PQLabel.setGeometry(26, 229, 291, 30)

        self.phanQuyenComboBox = QComboBox(AccountDetailPanel) 
        self.phanQuyenComboBox.setStyleSheet("""
                background-color: white;
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.phanQuyenComboBox.setGeometry(26, 270, 300, 35)
        for phanquyen in self.phanquyen_list:
            self.phanQuyenComboBox.addItem(phanquyen)
        self.phanQuyenComboBox.setCurrentIndex(-1)
        
        # Hủy
        self.cancelButton = QPushButton("Hủy", AccountDetailPanel)
        self.cancelButton.setGeometry(112, 600, 125, 50)
        self.cancelButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: White;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #EBEBEB;}"
                                        "QPushButton:pressed {background-color: #E0E0E0;}")
        self.cancelButton.clicked.connect(self.close) 
        
        # Cập nhật
        self.updateButton = QPushButton("Lưu", AccountDetailPanel)
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
            sql = "SELECT account.maNV, staff.tenNV, account.matkhau, account.phanquyen from account inner join staff on account.maNV = staff.maNV where account.maNV = %s"
            mycursor.execute(sql,(data,))
            # Lấy kết quả
            results  = mycursor.fetchall()
            for record in results:
                maNV, tenNV, matkhau, phanquyen = record
                account = Account.Account(maNV, tenNV, matkhau, phanquyen)
                self.account_list.append(account)
            # Đóng kết nối sau khi hoàn thành

            self.maNVInput.setText(str(account.getMaNV()))
            self.MKInput.setText(account.getMatkhau())
            
            phanquyen = account.getPhanquyen()
            self.phanQuyenComboBox.setCurrentText(phanquyen)
            
            self.tenNVInput.setText(account.getTenNV())

            db_connector.close()
        else:
            print("Failed to connect to database")

    def updateDB(self):
        maNV = self.maNVInput.text()
        matkhau = self.MKInput.text()
        phanquyen = self.phanQuyenComboBox.currentText()

        self.acc_dao = AccountDAO()
        self.acc_dao.update(maNV, matkhau, phanquyen)

    def showCancelButton(self):
        self.cancelButton.show()
