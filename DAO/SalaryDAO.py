from DAO.DBConnect import DBConnect
from DTO import Account
from PyQt6.QtWidgets import QMessageBox

class SalaryDAO:
       
    def add(self, maNV, ngay, thoigianlam, tongtien):
        # Add a new staff member to the database
        db_connector = DBConnect()
        try:
            mycursor = db_connector.connect()
            
            query = "INSERT INTO `salary`(`maNV`, `ngay`, `thoigianlam`, `tongtien`) VALUES (%s,%s,%s,%s)"
            
            values = (maNV, ngay, thoigianlam, tongtien)
            mycursor.execute(query, values)
            db_connector.connection.commit()
        finally:
            db_connector.close()
   