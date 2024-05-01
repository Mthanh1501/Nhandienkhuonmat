from PyQt6.QtWidgets import QWidget,QHBoxLayout
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication

from GUI import CheckInGUI,SidebarGUI,StaffGUI,DepartmentGUI,PositionGUI,AccountGUI,SalaryGUI,StatisticsGUI



class SwitchPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.createdWidgets = []
        self.initUI()

    def initUI(self):
        global sideBar,layout

        # Create a home panel widget
        self.setFixedSize(1080, 656)

        # Components
        sideBar = SidebarGUI.SidebarGUI()

        # Sidebar button event
        sideBar.panelCI.mousePressEvent = lambda event: self.chkInTab()
        sideBar.panelNV.mousePressEvent = lambda event: self.showTabStaff()
        sideBar.panelPB.mousePressEvent = lambda event: self.showTabDPM()
        sideBar.panelCV.mousePressEvent = lambda event: self.showTabPOS()
        sideBar.panelTaiKhoan.mousePressEvent = lambda event: self.showTabACC()
        sideBar.panelLuong.mousePressEvent = lambda event: self.showTabSalary()
        sideBar.panelTK.mousePressEvent = lambda event: self.showTabTK()

        # Layout
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(sideBar)
        layout.addWidget(sideBar, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)

    def chkInTab(self):
        self.closeAll()
        self.chkIn = CheckInGUI.CheckInGUI()
        layout.addWidget(self.chkIn)
        self.createdWidgets.append(self.chkIn)

    def showTabStaff(self):
        self.closeAll()
        self.tabStaff = StaffGUI.StaffGUI()
        layout.addWidget(self.tabStaff)
        self.createdWidgets.append(self.tabStaff)

    def showTabDPM(self):
        self.closeAll()
        self.tabDPM = DepartmentGUI.DepartmentGUI()
        layout.addWidget(self.tabDPM)
        self.createdWidgets.append(self.tabDPM)

    def showTabPOS(self):
        self.closeAll()
        self.tabPOS = PositionGUI.PositionGUI()
        layout.addWidget(self.tabPOS)
        self.createdWidgets.append(self.tabPOS)


    def showTabACC(self):
        self.closeAll()
        self.tabACC = AccountGUI.AccountGUI()
        layout.addWidget(self.tabACC)
        self.createdWidgets.append(self.tabACC)


    def showTabSalary(self):
        self.closeAll()
        self.tabSalary = SalaryGUI.SalaryGUI()
        layout.addWidget(self.tabSalary)
        self.createdWidgets.append(self.tabSalary)


    def showTabTK(self):
        self.closeAll()
        self.tabTK = StatisticsGUI.StatisticsGUI()
        layout.addWidget(self.tabTK)
        self.createdWidgets.append(self.tabTK)


    def closeAll(self):
        # Close only the widgets created by your application
        for widget in self.createdWidgets:
            widget.close()
        

  
