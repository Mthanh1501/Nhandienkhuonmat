from DAO.DBConnect import DBConnect
from DTO import Account
from PyQt6.QtWidgets import QMessageBox

class AccountDAO:
       
    def add(self, maNV, matkhau, phanquyen):
        # Add a new staff member to the database
        if self.validateInput(maNV, matkhau, phanquyen):
            db_connector = DBConnect()
            try:
                mycursor = db_connector.connect()

                query = "INSERT INTO `account`(`maNV`, `matkhau`, `phanquyen`) VALUES (%s,%s,%s) "

                values = (maNV, matkhau, phanquyen)
                mycursor.execute(query, values)
                db_connector.connection.commit()
                QMessageBox.information(None, "Thông báo", "Bạn đã thêm tài khoản thành công!")
            finally:
                db_connector.close()

    def validateInput(self, maNV, matkhau, phanquyen):
        if not all([maNV, matkhau, phanquyen]):
            QMessageBox.warning(None, "Nhắc nhở", 'Vui lòng điền đầy đủ thông tin')
            return False
        return True

    def update(self, maNV, matkhau, phanquyen):
        if self.validateUpdate(maNV, matkhau, phanquyen):
            db_connector = DBConnect()
            try:
                mycursor = db_connector.connect()
                # Update an existing staff member in the database
                query = "UPDATE account SET matkhau = %s, phanquyen = %s WHERE maNV = %s"
                values = (matkhau, phanquyen, maNV)
                mycursor.execute(query, values)
                db_connector.connection.commit()
                QMessageBox.information(None, "Thông báo", "Bạn đã sửa thông tin tài khoản thành công!")
            finally:
                db_connector.close()
    
    def validateUpdate(self, maNV, matkhau, phanquyen):
        if not all([matkhau, phanquyen]):
            QMessageBox.warning(None, "Nhắc nhở", 'Vui lòng điền đầy đủ thông tin')
            return False
        return True
    
    def delete(self, maNV):
        # Delete a staff member from the database
        db_connector = DBConnect()
        try:
            mycursor = db_connector.connect()
            # Update an existing staff member in the database
            query = "DELETE FROM account WHERE maNV=%s"
            values = (maNV,)
            mycursor.execute(query, values)
            db_connector.connection.commit()
        finally:
            db_connector.close()
