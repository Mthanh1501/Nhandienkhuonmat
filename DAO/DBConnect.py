import mysql.connector

class DBConnect:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "staffmanagement"
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        if self.connection.is_connected():
            print("Connected to database")
        else:
            print("Failed to connect to database")
        
        return self.connection.cursor()

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Connection closed")
