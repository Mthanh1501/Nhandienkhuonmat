from PyQt6.QtWidgets import QWidget, QVBoxLayout,QMessageBox

from BLL import SwitchPanel
from GUI import HeaderGUI,HomeGUI,LoginGUI



class initComponents(QWidget):
    def __init__(self,):
        super().__init__()
        self.createdWidgets = []
        self.initUI()

    def initUI(self):
        global header_widget, login_widget, home_widget, tab_widget, main_layout

        # Create a layout for the main widget
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Create the header widget
        header_widget = HeaderGUI.HeaderGUI()
        home_widget = HomeGUI.HomeGUI()
        login_widget = LoginGUI.LoginGUI()
        tab_widget = SwitchPanel.SwitchPanel()

        # Add widget
        main_layout.addWidget(header_widget)
        main_layout.addWidget(home_widget)
        
        # Event
        header_widget.login_button.clicked.connect(self.showLoginWidget)
        login_widget.loginButton.clicked.connect(self.checkLogin)
        login_widget.returnButton.clicked.connect(self.showHomeWidget)

    # Hiển thị widget đăng nhập
    def showLoginWidget(self):
        if header_widget.login_button.text() == 'Đăng nhập':
            print('Login')
            self.closePanel()
            main_layout.addWidget(login_widget)
            login_widget.show()
        else:
            print('Logout')
            self.closePanel()
            self.showHomeWidget()
            header_widget.label.setText('Welcome')
            header_widget.login_button.setText('Đăng nhập')

    # Hiển thị Home
    def showHomeWidget(self):
        print('Home')
        self.closePanel()
        main_layout.addWidget(home_widget)
        home_widget.show()

    # Hiển thị TabPanel
    def showTabWidget(self):
        print('Tab')
        self.closePanel()
        main_layout.addWidget(tab_widget)

    # Kiểm tra đăng nhập
    def checkLogin(self):
        print('Check login: ', end='')
        if login_widget.checkLogin():
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
        home_widget.close()
        login_widget.close()
        tab_widget.close()
