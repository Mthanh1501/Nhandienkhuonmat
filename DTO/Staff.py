class Staff:
    def __init__(self, maNV, tenNV, sDT, ngaySinh, gioiTinh, tenPB, tenCV, luong, hinhanh):
        self.__maNV = maNV
        self.__tenNV = tenNV
        self.__sDT = sDT
        self.__ngaySinh = ngaySinh
        self.__gioiTinh = gioiTinh
        # self.__maPB = maPB
        # self.__maCV = maCV
        self.__luong = luong
        self.__tenPB = tenPB
        self.__tenCV = tenCV
        self.__hinhanh = hinhanh

    # Getter methods
    def getMaNV(self):
        return self.__maNV

    def getTenNV(self):
        return self.__tenNV

    def getSDT(self):
        return self.__sDT

    def getNgaySinh(self):
        return self.__ngaySinh

    def getGioiTinh(self):
        return self.__gioiTinh

    def getTenPB(self):
        return self.__tenPB

    def getTenCV(self):
        return self.__tenCV

    def getLuong(self):
        return self.__luong

    def getHinhanh(self):
        return self.__hinhanh

    # Setter methods
    def setMaNV(self, maNV):
        self.__maNV = maNV

    def setTenNV(self, tenNV):
        self.__tenNV = tenNV

    def setSDT(self, sDT):
        self.__sDT = sDT

    def setNgaySinh(self, ngaySinh):
        self.__ngaySinh = ngaySinh

    def setGioiTinh(self, gioiTinh):
        self.__gioiTinh = gioiTinh

    def setTenPB(self, tenPB):
        self.__tenPB = tenPB

    def setTenCV(self, tenCV):
        self.__tenCV = tenCV

    def setLuong(self, luong):
        self.__luong = luong

    def setHinhanh(self, hinhanh):
        self.__hinhanh = hinhanh
