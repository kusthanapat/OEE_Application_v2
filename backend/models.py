# # for phpmysql
# import mysql.connector
# from mysql.connector import Error

# for postgreSQL
import psycopg2
from psycopg2 import Error

def create_connection():
    """Create a database connection"""
    try:
        # for phpmysql
        # connection = mysql.connector.connect(
        #     host='localhost',
        #     port=3306,
        #     user='root',
        #     password='',  # Empty password as per your config
        #     database='machines_database'
        # )
        
        # for postgreSQL
        connection = psycopg2.connect(
            host='10.0.0.158',
            port=5432,
            user='admin',
            password='Admin_password_2568',  # Empty password as per your config
            database='mydatabase'
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
            INSERT INTO "user" (firstName, lastName, username, password)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (first_name, last_name, username, password))
        
        connection.commit()
        print("User added successfully!")

    except Error as e:
        print(str(e))
        print(f"Error: {e}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")