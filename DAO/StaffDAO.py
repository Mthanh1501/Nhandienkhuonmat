from DAO.DBConnect import DBConnect
from DTO import Staff
from PyQt6.QtWidgets import QMessageBox
import re

class StaffDAO:
       
    def add(self, maNV, tenNV, sDT, ngaySinh, gioiTinh, maPB,maCV,luong,trangthai,img):
        # Add a new staff member to the database
        if self.validateInput(maNV, tenNV, sDT, ngaySinh, gioiTinh, maPB, maCV, luong, trangthai,img) and self.checkExistingStaff(maNV, sDT):
            db_connector = DBConnect()
            try:
                mycursor = db_connector.connect()
                query = "INSERT INTO `staff`(`maNV`, `tenNV`, `sdt`, `ngaySinh`, `gioiTinh`, `maPB`, `maCV`, `luong`, `trangthai`,`hinhanh`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                image_bytes = bytes(img)
                values = (maNV, tenNV, sDT, ngaySinh, gioiTinh, maPB, maCV, luong, trangthai,image_bytes)
                mycursor.execute(query, values)
                db_connector.connection.commit()
                QMessageBox.information(None, "Thông báo", "Bạn đã thêm nhân viên thành công!")
            finally:
                db_connector.close()
            
    def validateInput(self, maNV, tenNV, sDT, ngaySinh, gioiTinh, maPB,maCV,luong,trangthai,img):
        # kiểm tra các trường nếu chưa được nhập
        if not all([tenNV, sDT, ngaySinh, maPB,maCV,luong,trangthai]):
            QMessageBox.warning(None, "Nhắc nhở", 'Vui lòng điền đầy đủ thông tin')
            return False
        # kiểm tra định dạng số điện thoại
        if not re.match(r'^0\d{9}$', sDT):
            QMessageBox.warning(None, "Nhắc nhở", 'Số điện thoại không hợp lệ. Số điện thoại phải có định dạng là 10 chữ số và bắt đầu bằng số 0')
            return False
        # kiểm tra hợp lệ lương của nhân viên
        try:
            luong_fl = float(luong)
        except ValueError:
            QMessageBox.warning(None, "Nhắc nhở", "Lương vừa nhập vào không hợp lệ. Lương của nhân viên phải là chữ số")
            return False
        if luong_fl <= 0:
            QMessageBox.warning(None, "Nhắc nhở", 'Lương của nhân viên phải là một số lớn hơn hoặc bằng 0')
            return False
        # kiểm tra đã chọn chức vụ chưa
        if maCV == 0:
            QMessageBox.warning(None, "Nhắc nhở", 'Vui lòng chọn chức vụ cho nhân viên')
            return False
        #kiểm tra đã chọn phòng ban chưa
        if maPB == 0:
            QMessageBox.warning(None, "Nhắc nhở", 'Vui lòng chọn phòng ban cho nhân viên')
            return False
        return True
    
    def checkExistingStaff(self, maNV, sDT):
        db_connector = DBConnect()
        try:
            mycursor = db_connector.connect()

            # kiểm tra các nhân viên có trạng thái là 1 (đang làm việc)
            # không trùng mã nhân viên và không trùng số điện thoại
            check_query = "SELECT maNV, sdt FROM staff WHERE trangthai = 1 AND (maNV = %s OR sdt = %s)"
            mycursor.execute(check_query, (maNV, sDT))
            existing_staff_status1 = mycursor.fetchall()

            if existing_staff_status1:
                for staff in existing_staff_status1:
                    if staff[0] == maNV:
                        QMessageBox.warning(None, "Nhắc nhở", 'Mã nhân viên đã tồn tại')
                        return False
                    if staff[1] == sDT:
                        QMessageBox.warning(None, "Nhắc nhở", 'Số điện thoại đã tồn tại')
                        return False
            
            # kiểm tra các nhân viên có trạng thái là 0 (đã thôi việc)
            # không trùng mã nhân viên (cho trùng số điện thoại vì có thể nhận nhân viên đó vào làm một lần nữa)
            check_query = "SELECT maNV FROM staff WHERE trangthai = 0 AND maNV = %s"
            mycursor.execute(check_query, (maNV,))
            existing_staff_status0 = mycursor.fetchone()

            if existing_staff_status0:
                QMessageBox.warning(None, "Nhắc nhở", 'Mã nhân viên đã tồn tại')
                return False

            return True
        finally:
            db_connector.close()

    def update(self, maNV, tenNV, sDT, ngaySinh, gioiTinh, maPB,maCV,luong,img):
        if self.validateUpdate(maNV, tenNV, sDT, ngaySinh, gioiTinh, maPB,maCV,luong,img):
            db_connector = DBConnect()
            try:
                mycursor = db_connector.connect()
                # Update an existing staff member in the database
                query = "UPDATE `staff` SET `tenNV`=%s,`sdt`=%s,`ngaySinh`=%s,`gioiTinh`=%s,`maPB`=%s,`maCV`=%s,`luong`=%s, `hinhanh` =%s WHERE `staff`.`maNV` = %s"
                image_bytes = bytes(img)
                values = (tenNV, sDT, ngaySinh, gioiTinh, maPB,maCV,luong,image_bytes,maNV)
                mycursor.execute(query, values)
                db_connector.connection.commit()
            finally:
                db_connector.close()
    
    def validateUpdate(self, maNV, tenNV, sDT, ngaySinh, gioiTinh, maPB,maCV,luong,img):
        # kiểm tra xem có nhập tên nhân viên mới hay ko 
        if not tenNV:
            QMessageBox.warning(None, "Nhắc nhở", 'Vui lòng nhập tên nhân viên')
            return False
        # kiểm tra xem có nhập số điện thoại mới hay không
        if not sDT:
            QMessageBox.warning(None, "Nhắc nhở", 'Vui lòng nhập số điện thoại')
            return False
        else:
            if not re.match(r'^0\d{9}$', sDT):
                QMessageBox.warning(None, "Nhắc nhở", 'Số điện thoại không hợp lệ. Số điện thoại phải có định dạng là 10 chữ số và bắt đầu bằng số 0')
                return False
            else:
                db_connector = DBConnect()
                try:
                    mycursor = db_connector.connect()
                    query = "SELECT sDT FROM staff WHERE sDT = %s AND maNV != %s"
                    mycursor.execute(query, (sDT,maNV))
                    existing_phone = mycursor.fetchone()

                    if existing_phone:
                        QMessageBox.warning(None, "Nhắc nhở", 'Số điện thoại đã tồn tại')
                        return False
                finally:
                    db_connector.close()

        if not luong:
            QMessageBox.warning(None, "Nhắc nhở", 'Vui lòng nhập tên nhân viên')
            return False
        else:
            try:
                luong_fl = float(luong)
            except ValueError:
                QMessageBox.warning(None, "Nhắc nhở", "Lương vừa nhập vào không hợp lệ. Lương của nhân viên phải là chữ số")
                return False
            if luong_fl <= 0:
                QMessageBox.warning(None, "Nhắc nhở", 'Lương của nhân viên phải là một số lớn hơn hoặc bằng 0')
                return False
        return True
            
    
    def delete(self, maNV):
        # Delete a staff member from the database
        db_connector = DBConnect()
        try:
            mycursor = db_connector.connect()
            # Update an existing staff member in the database
            query = "UPDATE staff set trangthai = 0 where maNV=%s"
            values = (maNV,)
            mycursor.execute(query, values)
            db_connector.connection.commit()
        finally:
            db_connector.close()