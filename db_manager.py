import mysql.connector

class DBManager:
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': 'mere22',
            'host': 'localhost',
            'database': 'filme',
            'raise_on_warnings': True
        }
        self.conn = None

    def connect(self):
        """Deschide conexiunea"""
        self.conn = mysql.connector.connect(**self.config)
        return self.conn

    def disconnect(self):
        """Inchide conexiunea"""
        if self.conn and self.conn.is_connected():
            self.conn.close()

    def select(self, query, params=None):
        """Pentru SELECT-uri care returneaza mai multe randuri (tabele)"""
        self.connect()
        cursor = self.conn.cursor(dictionary=True) # Returneaza datele ca dictionar {'coloana': valoare}
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        cursor.close()
        self.disconnect()
        return result

    def select_one(self, query, params):
        """Pentru SELECT-uri care returneaza un singur rand (modificare)"""
        self.connect()
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        self.disconnect()
        return result

    def execute(self, query, params):
        """Pentru INSERT, UPDATE, DELETE"""
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit() # Salvam modificarile
        cursor.close()
        self.disconnect()