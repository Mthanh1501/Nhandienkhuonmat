from DAO.DBConnect import DBConnect


class CheckInDAO:
       
    def add(self, maNV, vaoCa):
        # Add a new staff member to the database
        db_connector = DBConnect()
        try:
            mycursor = db_connector.connect()

            query = "INSERT INTO `chamcong` (`maCK`, `maNV`, `vaoCa`, `raCa`) VALUES (NULL, %s,%s, NULL)"

            values = (maNV, vaoCa)
            mycursor.execute(query, values)
            db_connector.connection.commit()
        finally:
            db_connector.close()