from PyQt6.QtWidgets import QWidget, QVBoxLayout,QMessageBox
from PyQt6.QtCore import Qt

from BLL import SwitchPanel
from GUI import HeaderGUI,HomeGUI,LoginGUI,CheckInGUI

class initComponents(QWidget):
    def __init__(self,):
        super().__init__()
        self.createdWidgets = []
        self.initUI()

    def initUI(self):
        global main_layout, header_widget

        # Create a layout for the main widget
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        header_widget = HeaderGUI.HeaderGUI()

        # Add widget
        main_layout.addWidget(header_widget)
        self.showHomeWidget()

        header_widget.login_button.clicked.connect(self.showLoginWidget)

    def showHomeWidget(self):
        self.closePanel()
        self.home_widget = HomeGUI.HomeGUI()
        main_layout.addWidget(self.home_widget)
        self.home_widget.show()
        self.createdWidgets.append(self.home_widget)
        self.home_widget.panelCI.mousePressEvent = lambda event: self.chkInTab() 


    # Hiển thị widget đăng nhập
    def showLoginWidget(self):

        if  header_widget.login_button.text() == 'Đăng nhập':
            print('Login')
            self.closePanel()
            self.login_widget = LoginGUI.LoginGUI()
            main_layout.addWidget(self.login_widget)
            self.login_widget.show()
            self.login_widget.loginButton.clicked.connect(self.checkLogin)
            self.login_widget.returnButton.clicked.connect(self.showHomeWidget)
            self.createdWidgets.append(self.login_widget)
        else:
            print('Logout')
            self.closePanel()
            self.showHomeWidget()
            header_widget.label.setText('Welcome')
            header_widget.login_button.setText('Đăng nhập')

    def chkInTab(self):
        self.closePanel()
        self.chkIn = CheckInGUI.CheckInGUI()
        main_layout.addWidget(self.chkIn)
        main_layout.setAlignment(self.chkIn,Qt.AlignmentFlag.AlignCenter)
        self.createdWidgets.append(self.chkIn)

    # Hiển thị TabPanel
    def showTabWidget(self):
        self.tab_widget = SwitchPanel.SwitchPanel()
        print('Tab')
        self.closePanel()
        main_layout.addWidget(self.tab_widget)
        self.createdWidgets.append(self.tab_widget)

    # Kiểm tra đăng nhập
    def checkLogin(self):
        print('Check login: ', end='')
        if self.login_widget.checkLogin():
            self.showTabWidget()
            header_widget.label.setText('Quản Lý Nhân Sự')
            header_widget.login_button.setText('Đăng xuất')
        else:
            QMessageBox.information(self, "Login", "Sai username hoặc mật khẩu")
            self.showTabWidget()
            header_widget.label.setText('Quản Lý Nhân Sự')
            header_widget.login_button.setText('Đăng xuất')
            
    # Đóng Widget
    def closePanel(self):
        # Close only the widgets created by your application
        for widget in self.createdWidgets:
                widget.close()
