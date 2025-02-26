import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_DATABASE')
        }

    def create_connection(self):
        try:
            connection = mysql.connector.connect(**self.config)
            return connection
        except Error as e:
            raise Exception(f"Error connecting to database: {e}")

    def create_database(self):
        try:
            connection = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=self.config['password'] or ''
            )
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS indian_express")
            cursor.close()
            connection.close()
        except Error as e:
            raise Exception(f"Error creating database: {e}")
