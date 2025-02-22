import streamlit as st
import mysql.connector

class DatabaseConnection:
    def __init__(self):
        self.config = {
            'host': st.secrets.db_credentials.host,
            'user': st.secrets.db_credentials.user,
            'password': st.secrets.db_credentials.password,
            'database': st.secrets.db_credentials.database
        }
    
    def create_connection(self):
        try:
            connection = mysql.connector.connect(**self.config)
            return connection
        except Exception as e:
            raise Exception(f"Error connecting to database: {e}")
    
    def create_database(self):
        try:
            # Ensure password is set correctly if it's empty in secrets.toml.
            password = self.config['password'] or ''
            
            connection = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=password
            )
            
            cursor = connection.cursor()
            
            # Create database if it doesn't exist.
            cursor.execute("CREATE DATABASE IF NOT EXISTS indian_express")
            
            cursor.close()
            
            # Close the initial connection after creating the database.
            
            # Reconnect with the newly created database name if needed for further operations.
        
        except Exception as e:
        
          raise Exception(f"Error creating database: {e}")

