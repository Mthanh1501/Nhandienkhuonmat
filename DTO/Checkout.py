class Checkout:
    def __init__(self, maCKIN, maNV, raCA):
        self.maCKIN = maCKIN
        self.maNV = maNV
        self.raCA = raCA


    # Getter methods
    def getMaCKIN(self):
        return self.maCKIN
    
    def getMaNV(self):
        return self.maNV
    
    def getRaCA(self):
        return self.raCA

    # Setter methods
    def setMaCKIN(self, maCKIN):
        self.maCKIN = maCKIN
        
    def setMaNV(self, maNV):
        self.maNV = maNV
        
    def setRaCA(self, raCA):
        self.raCA = raCA
    