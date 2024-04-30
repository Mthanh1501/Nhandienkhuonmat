class Department:
    def __init__(self, maPB, tenPB, diaDiemPB):
        self.maPB = maPB
        self.tenPB = tenPB
        self.diaDiemPB = diaDiemPB

    # Getter methods
    def getMaPB(self):
        return self.maPB

    def getTenPB(self):
        return self.tenPB

    def getDiaDiemPB(self):
        return self.diaDiemPB

    # Setter methods
    def setMaPB(self, maPB):
        self.maPB = maPB

    def setTenPB(self, tenPB):
        self.tenPB = tenPB

    def setDiaDiemPB(self, diaDiemPB):
        self.diaDiemPB = diaDiemPB
