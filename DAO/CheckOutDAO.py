from DAO.DBConnect import DBConnect


class CheckOutDAO:

    def add(self, maNV, raCa, ngayhomnay):
        # Add a new staff member to the database
        db_connector = DBConnect()
        try:
            mycursor = db_connector.connect()

            # Update the first row
            update_query = """
                UPDATE `chamcong`
                SET `raCa` = %s
                WHERE `maNV` = %s AND `vaoCa` LIKE %s
                LIMIT 1;
            """
            update_values = (raCa, maNV, ngayhomnay +'%')
            mycursor.execute(update_query, update_values)
            db_connector.connection.commit()

            # Delete all other rows
            delete_query = """
                DELETE FROM `chamcong`
                WHERE `maNV` = %s AND `vaoCa` LIKE %s AND `raCa` IS NULL;
            """
            delete_values = (maNV, ngayhomnay +'%')
            mycursor.execute(delete_query, delete_values)
            db_connector.connection.commit()

        finally:
            db_connector.close()
