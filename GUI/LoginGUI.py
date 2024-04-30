from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit
from PyQt6.QtCore import Qt
import mysql.connector
from DAO.DBConnect import DBConnect

class LoginGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a login panel widget
        self.setFixedSize(1080, 657)

        loginPanel = QWidget(self)  # Specify parent widget
        loginPanel.setStyleSheet("background-color: white;")
        loginPanel.setFixedSize(400, 420)
        loginPanel.move(340, 89)

        userLabel = QLabel("UserID", loginPanel)
        userLabel.setStyleSheet("font-size: 16pt;")
        userLabel.setGeometry(54, 60, 291, 25)

        self.userInput = QLineEdit(loginPanel)
        self.userInput.setStyleSheet("""
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.userInput.setGeometry(54, 101, 300, 35)

        passlabel = QLabel("Password", loginPanel)
        passlabel.setStyleSheet("font-size: 16pt;")
        passlabel.setGeometry(54, 152, 291, 25)

        self.passInput = QLineEdit(loginPanel)
        self.passInput.setStyleSheet("""
                border: 2px solid #B8B8B8;
                border-radius: 5px;""")
        self.passInput.setGeometry(54, 193, 300, 35)

        self.returnButton = QPushButton("Quay lại", loginPanel)
        self.returnButton.setGeometry(35, 295, 140, 40)
        self.returnButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: #D9D9D9;min-width: 80px;}"
                                        "QPushButton:hover {background-color: #CDCDCD;}"
                                        "QPushButton:pressed {background-color: darkgray;}")

        self.loginButton = QPushButton("Đăng nhập", loginPanel)
        self.loginButton.setGeometry(225, 295, 140, 40)
        self.loginButton.setStyleSheet("QPushButton {border-radius: 5px;background-color: #D9D9D9;min-width: 80px;}"
                                       "QPushButton:hover {background-color: #CDCDCD;}"
                                       "QPushButton:pressed {background-color: darkgray;}")


   

    def checkLogin(self):
        us = self.userInput.text()
        pw = self.passInput.text()

        try:
            # Kết nối đến cơ sở dữ liệu
            db_connector = DBConnect()
            mycursor = db_connector.connect()

            if mycursor is not None:
                # Thực hiện truy vấn kiểm tra đăng nhập
                query = "SELECT * FROM account WHERE maNV = %s AND matKhau = %s"
                print(query)
                mycursor.execute(query, (us, pw))
                row = mycursor.fetchone()
                print(row)

                if row:
                    print('Success')
                    return True
                else:
                    print('Failed')
                    return False
        except mysql.connector.Error as error:
            print("Lỗi kết nối đến cơ sở dữ liệu:", error)
        finally:
            if mycursor is not None:
                mycursor.close()
                print("Kết thúc kết nối đến cơ sở dữ liệu")

