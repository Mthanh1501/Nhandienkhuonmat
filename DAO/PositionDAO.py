from DAO.DBConnect import DBConnect
from DTO import Staff
from PyQt6.QtWidgets import QMessageBox

class PositionDAO:
       
    def add(self, maCV, tenCV):
        # Add a new staff member to the database
        if self.validateInput(maCV, tenCV) and self.checkExistingPosition(tenCV):
            db_connector = DBConnect()
            try:
                mycursor = db_connector.connect()

                query = "INSERT INTO `position`(`maCV`, `tenCV) VALUES (%s,%s)"

                values = (maCV, tenCV)
                mycursor.execute(query, values)
                db_connector.connection.commit()
                QMessageBox.information(None, "Thông báo", "Bạn đã thêm chức vụ thành công!")
            finally:
                db_connector.close()

    def validateInput(self, maCV, tenCV):
        if not tenCV:
            QMessageBox.warning(None, "Nhắc nhở", 'Vui lòng điền đầy đủ thông tin')
            return False
        return True
    
    def checkExistingPosition(self, tenCV):
        db_connector = DBConnect()
        try:
            mycursor = db_connector.connect()
            query = "SELECT tenCV FROM position WHERE tenCV = %s"
            mycursor.execute(query, (tenCV,))
            existing_department = mycursor.fetchone()
            
            if existing_department:
                QMessageBox.warning(None, "Nhắc nhở", 'Đã tồn tại chức vụ này, vui lòng thử nhập tên chức vụ khác!')
                return False
            return True
        finally:
            db_connector.close()

    def update(self, maCV, tenCV):
        if self.validateUpdate(maCV, tenCV):
            db_connector = DBConnect()
            try:
                mycursor = db_connector.connect()
                # Update an existing staff member in the database
                query = "UPDATE `position` SET `tenCV`=%sWHERE `position`.`maCV` = %s"
                values = (tenCV,maCV)
                mycursor.execute(query, values)
                db_connector.connection.commit()
                QMessageBox.information(None, "Thông báo", "Bạn đã sửa thông tin chức vụ thành công!")
            finally:
                db_connector.close()
    
    def validateUpdate(self, maCV, tenCV):
        if not tenCV:
            QMessageBox.warning(None, "Nhắc nhở", 'Vui lòng điền đầy đủ thông tin')
            return False
        db_connector = DBConnect()
        try:
            mycursor = db_connector.connect()
            query = "SELECT tenCV FROM position WHERE tenCV = %s and maCV != %s"
            mycursor.execute(query, (tenCV,maCV))
            existing_department = mycursor.fetchone()
            
            if existing_department:
                QMessageBox.warning(None, "Nhắc nhở", 'Đã tồn tại chức vụ này, vui lòng thử nhập tên chức vụ khác!')
                return False
            return True
        finally:
            db_connector.close()
        return True
    def delete(self, maCV):
        # Delete a staff member from the database
        db_connector = DBConnect()
        try:
            mycursor = db_connector.connect()
            # Update an existing staff member in the database
            query = "DELETE FROM position WHERE maCV=%s"
            values = (maCV,)
            mycursor.execute(query, values)
            db_connector.connection.commit()
        finally:
            db_connector.close()
