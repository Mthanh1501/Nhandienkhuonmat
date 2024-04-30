from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout
from PyQt6.QtCore import Qt


class SidebarGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Create a sidebar panel widget
        self.setFixedSize(183, 656)

        sidebarPanel = QWidget(self)  # Specify parent widget
        sidebarPanel.setStyleSheet("background-color: white;")
        sidebarPanel.setFixedSize(183, 656)
        sidebarPanel.move(0, 0)

        # Create a grid layout for panels
        grid_layout = QGridLayout(sidebarPanel)

        # Check in
        self.panelCI = QWidget()
        self.panelCI.setFixedSize(160, 49)
        self.panelCI.setStyleSheet("QWidget {border-radius: 5px;background-color: #D9D9D9;}"
                          "QWidget:hover {background-color: #CDCDCD;}")
        label_CI = QLabel("Check In", self.panelCI)
        label_CI.setFixedSize(160, 49)
        label_CI.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.panelCI)

        # Check out
        # self.panelCK = QWidget()
        # self.panelCK.setFixedSize(160, 49)
        # self.panelCK.setStyleSheet("QWidget {border-radius: 5px;background-color: #D9D9D9;}"
        #                   "QWidget:hover {background-color: #CDCDCD;}")
        # label_CK = QLabel("Check Out", self.panelCK)
        # label_CK.setFixedSize(160, 49)
        # label_CK.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # grid_layout.addWidget(self.panelCK)

        # Nhân viên
        self.panelNV = QWidget()
        self.panelNV.setFixedSize(160, 49)
        self.panelNV.setStyleSheet("QWidget {border-radius: 5px;background-color: #D9D9D9;}"
                          "QWidget:hover {background-color: #CDCDCD;}")
        label_NV = QLabel("Nhân Viên", self.panelNV)
        label_NV.setFixedSize(160, 49)
        label_NV.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.panelNV)

        # Phòng ban
        self.panelPB = QWidget()
        self.panelPB.setFixedSize(160, 49)
        self.panelPB.setStyleSheet("QWidget {border-radius: 5px;background-color: #D9D9D9;}"
                          "QWidget:hover {background-color: #CDCDCD;}")
        label_PB = QLabel("Phòng Ban", self.panelPB)
        label_PB.setFixedSize(160, 49)
        label_PB.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.panelPB)

        # Thống kê
        self.panelTK = QWidget()
        self.panelTK.setFixedSize(160, 49)
        self.panelTK.setStyleSheet("QWidget {border-radius: 5px;background-color: #D9D9D9;}"
                          "QWidget:hover {background-color: #CDCDCD;}")
        label_TK = QLabel("Thống Kê", self.panelTK)
        label_TK.setFixedSize(160, 49)
        label_TK.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.panelTK)

        # Lương
        self.panelLuong = QWidget()
        self.panelLuong.setFixedSize(160, 49)
        self.panelLuong.setStyleSheet("QWidget {border-radius: 5px;background-color: #D9D9D9;}"
                             "QWidget:hover {background-color: #CDCDCD;}")
        label_Luong = QLabel("Bảng Lương", self.panelLuong)
        label_Luong.setFixedSize(160, 49)
        label_Luong.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.panelLuong)

        # Chức vụ
        self.panelCV = QWidget()
        self.panelCV.setFixedSize(160, 49)
        self.panelCV.setStyleSheet("QWidget {border-radius: 5px;background-color: #D9D9D9;}"
                          "QWidget:hover {background-color: #CDCDCD;}")
        label_CV = QLabel("Chức Vụ", self.panelCV)
        label_CV.setFixedSize(160, 49)
        label_CV.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.panelCV)

        # Tai khoản
        self.panelTaiKhoan = QWidget()
        self.panelTaiKhoan.setFixedSize(160, 49)
        self.panelTaiKhoan.setStyleSheet("QWidget {border-radius: 5px;background-color: #D9D9D9;}"
                                "QWidget:hover {background-color: #CDCDCD;}")
        label_TaiKhoan = QLabel("Tài Khoản", self.panelTaiKhoan)
        label_TaiKhoan.setFixedSize(160, 49)
        label_TaiKhoan.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(self.panelTaiKhoan)
