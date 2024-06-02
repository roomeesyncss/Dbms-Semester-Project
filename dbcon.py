
import pyodbc
from config import DATABASE_CONFIG

class DatabaseConnection:
    def __init__(self):
        self.server_name = DATABASE_CONFIG['server_name']
        self.database_name = DATABASE_CONFIG['database_name']
        self.trusted_connection = DATABASE_CONFIG['trusted_connection']
        self.connection = None

    def create_connection(self):
        connection_string = f'DRIVER={{SQL Server}};SERVER={self.server_name};DATABASE={self.database_name};Trusted_Connection={self.trusted_connection};'
        self.connection = pyodbc.connect(connection_string)
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
