# db_utils.py
import mysql.connector
from mysql.connector import Error

def create_connection():
    """Create a database connection"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Empty password as per your config
            database='machines_database'
        )
        
        if connection.is_connected():
            return connection
            
    except Error as e:
        print(f"Error: {e}")
        return None


def add_user(first_name, last_name, username, password):
    """Add a user to the 'user' table"""
    connection = create_connection()

    if connection is None:
        print("Unable to connect to the database.")
        return

    try:
        cursor = connection.cursor()

        # Query to insert new user
        insert_query = """
            INSERT INTO user (firstName, lastName, username, password)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (first_name, last_name, username, password))
        
        connection.commit()
        print("User added successfully!")

    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")