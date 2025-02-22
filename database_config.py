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
            password = self.config['password'] or ''
            
            # Connect without specifying a database first.
            initial_connection = mysql.connector.connect(
                host=self.config['host'],
                user=self.config['user'],
                password=password
            )
            
            cursor = initial_connection.cursor()
            
            # Create database if it doesn't exist.
            cursor.execute("CREATE DATABASE IF NOT EXISTS indian_express")
            
            cursor.close()
            
            # Close initial connection.
        
        except Exception as e:
          raise Exception(f"Error creating database: {e}")

# Example usage for creating and then connecting to the newly created DB.
if __name__ == "__main__":
    db_conn = DatabaseConnection()
    
    db_conn.create_database()

    # Update config with new DB name before reconnecting.
    db_conn.config['database'] = "indian_express"
    
    conn_with_db_name = db_conn.create_connection()

