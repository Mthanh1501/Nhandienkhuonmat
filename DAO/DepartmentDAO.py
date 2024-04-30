from DAO.DBConnect import DBConnect
from DTO import Department
from PyQt6.QtWidgets import QMessageBox

class DepartmentDAO:
       
    def add(self, maPB, tenPB, diaDiem):
        # Add a new staff member to the database
        if self.validateInput(maPB, tenPB, diaDiem) and self.checkExistingDepartment(tenPB, diaDiem):
            db_connector = DBConnect()
            try:
                mycursor = db_connector.connect()
                query = "INSERT INTO `department`(`maPB`, `tenPB`, `diadiem`) VALUES (%s,%s,%s)"
                values = (maPB, tenPB, diaDiem)
                mycursor.execute(query, values)
                db_connector.connection.commit()
                QMessageBox.information(None, "Thông báo", "Bạn đã thêm phòng ban thành công!")
            finally:
                db_connector.close()
            
    def validateInput(self, maPB, tenPB, diaDiem):
        if not all([tenPB, diaDiem]):
            QMessageBox.warning(None, "Nhắc nhở", 'Vui lòng điền đầy đủ thông tin')
            return False
        return True
    
    def checkExistingDepartment(self, tenPB, diaDiem):
        db_connector = DBConnect()
        try:
            mycursor = db_connector.connect()
            query = "SELECT tenPB, diaDiem FROM department WHERE tenPB = %s and diaDiem = %s"
            mycursor.execute(query, (tenPB,diaDiem))
            existing_department = mycursor.fetchone()
            
            if existing_department:
                QMessageBox.warning(None, "Nhắc nhở", 'Phòng ban tại địa điểm vừa nhập đã tồn tại. Vui lòng sửa lại tên phòng ban hoặc địa điểm!')
                return False
            return True
        finally:
            db_connector.close()

    def update(self, maPB, tenPB, diaDiem):
        if self.validateUpdate(maPB, tenPB, diaDiem):
            db_connector = DBConnect()
            try:
                mycursor = db_connector.connect()
                # Update an existing staff member in the database
                query = "UPDATE department SET tenPB = %s, diaDiem = %s WHERE department.maPB = %s"
                values = (tenPB, diaDiem, maPB)
                mycursor.execute(query, values)
                db_connector.connection.commit()
                QMessageBox.information(None, "Thông báo", "Bạn đã sửa thông tin phòng ban thành công!")
            finally:
                db_connector.close()
    
    def validateUpdate(self, maPB, tenPB, diaDiem):
        if not all([tenPB, diaDiem]):
            QMessageBox.warning(None, "Nhắc nhở", 'Vui lòng điền đầy đủ thông tin')
            return False
        db_connector = DBConnect()
        try:
            mycursor = db_connector.connect()
            query = "SELECT tenPB, diaDiem FROM department WHERE tenPB = %s and diaDiem = %s and maPB != %s"
            mycursor.execute(query, (tenPB,diaDiem,maPB))
            existing_department = mycursor.fetchone()
            
            if existing_department:
                QMessageBox.warning(None, "Nhắc nhở", 'Phòng ban tại địa điểm vừa nhập đã tồn tại. Vui lòng sửa lại tên phòng ban hoặc địa điểm!')
                return False
            return True
        finally:
            db_connector.close()
        return True
    def delete(self, maPB):
        # Delete a staff member from the database
        db_connector = DBConnect()
        try:
            mycursor = db_connector.connect()
            # Update an existing staff member in the database
            query = "DELETE FROM department WHERE maPB=%s"
            values = (maPB,)
            mycursor.execute(query, values)
            db_connector.connection.commit()
        finally:
            db_connector.close()
