class Account:
    def __init__(self, maNV, tenNV, matkhau, phanquyen):
        self.maNV = maNV
        self.matkhau = matkhau
        self.phanquyen = phanquyen
        self.tenNV = tenNV
    
    # getter
    def getMaNV(self):
        return self.maNV
    
    def getMatkhau(self):
        return self.matkhau
    
    def getPhanquyen(self):
        return self.phanquyen
    
    def getTenNV(self):
        return self.tenNV

    # setter
    def setMaNV(self, maNV):
        self.maNV = maNV
    
    def setTenNV(self, tenNV):
        self.tenNV = tenNV 
    
    def setMatkhau(self, matkhau):
        self.matkhau = matkhau
    
    def setPhanquyen(self, phanquyen):
        self.phanquyen = phanquyen
    