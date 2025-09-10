# # db_utils.py

# # # for phpmysql
# # import mysql.connector
# # from mysql.connector import Error

# # for postgreSQL
# import psycopg2
# from psycopg2 import Error

# def create_connection():
#     """Create a database connection"""
#     try:
#         # # for phpmysql
#         # connection = mysql.connector.connect(
#         #     host='localhost',
#         #     port=3306,
#         #     user='root',
#         #     password='',  # Empty password as per your config
#         #     database='machines_database'
#         # )
        
#         # for postgreSQL
#         connection = psycopg2.connect(
#             host='10.0.0.158',
#             port=5432,
#             user='admin',
#             password='Admin_password_2568',
#             database='mydatabase'
#         )
        
#         if connection.is_connected():
#             return connection
            
#     except Error as e:
#         print(f"Error: {e}")
#         return None


# def add_user(first_name, last_name, username, password):
#     """Add a user to the 'user' table"""
#     connection = create_connection()

#     if connection is None:
#         print("Unable to connect to the database.")
#         return

#     try:
#         cursor = connection.cursor()

#         # Query to insert new user
#         insert_query = """
#             INSERT INTO user (firstName, lastName, username, password)
#             VALUES (%s, %s, %s, %s)
#         """
#         cursor.execute(insert_query, (first_name, last_name, username, password))
        
#         connection.commit()
#         print("User added successfully!")

#     except Error as e:
#         print(f"Error: {e}")
    
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
#             # print("MySQL connection is closed.")
#             print("postgreSSQL connection is closed.")





# code V2
# import psycopg2
# from psycopg2 import Error, extras

# # Replace with your PostgreSQL database connection details
# DB_NAME = "mydatabase"
# DB_USER = "admin"
# DB_PASS = "Admin_password_2568"
# DB_HOST = "10.0.0.158" # or your PostgreSQL host
# DB_PORT = "5432"

# def create_connection():
#     """Create a connection to the PostgreSQL database."""
#     connection = None
#     try:
#         connection = psycopg2.connect(
#             dbname=DB_NAME,
#             user=DB_USER,
#             password=DB_PASS,
#             host=DB_HOST,
#             port=DB_PORT
#         )
#         print("Connection to PostgreSQL DB successful")
#         return connection
#     except Error as e:
#         print(str(e))
#         print(f"The error '{e}' occurred")
#         return None

# def get_user_by_username(username):
#     """Fetch a user from the database by their username."""
#     connection = create_connection()
#     user = None
#     if connection:
#         try:
#             cursor = connection.cursor(cursor_factory=extras.DictCursor)
#             query = "SELECT * FROM public.user WHERE username = %s"
#             cursor.execute(query, (username,))
#             user = cursor.fetchone()
#         except Error as e:
#             print(str(e))
#             print(f"Database error while fetching user: {e}")
#         finally:
#             if connection:
#                 cursor.close()
#                 connection.close()
#     return user

# def add_user(first_name, last_name, username, hashed_password):
#     """Add a new user to the database."""
#     connection = create_connection()
#     if connection:
#         try:
#             cursor = connection.cursor()
#             # The query has been updated to use the correct column names (firstName, lastName)
#             # and now includes the TimeStamp column. We use the NOW() function to let the
#             # database handle the timestamp generation.
#             insert_query = """
#             INSERT INTO "user" (firstName, lastName, username, password, TimeStamp)
#             VALUES (%s, %s, %s, %s, NOW())
#             """
#             # Use a tuple for the values to be inserted, using the hashed password
#             values = (first_name, last_name, username, hashed_password)
#             cursor.execute(insert_query, values)
#             connection.commit()
#             print("User added successfully.")
#         except Error as e:
#             # Rollback the transaction on error
#             connection.rollback()
#             # Raise the exception so it can be caught in the calling function (routes.py)
#             print(str(e))
#             raise Exception(f"Failed to add user: {e}")
#         finally:
#             if connection:
#                 cursor.close()
#                 connection.close()









# code V3
# db_utils.py

# # for phpmysql
# import mysql.connector
# from mysql.connector import Error

# for postgreSQL
import psycopg2
from psycopg2 import Error

def create_connection():
    """Create a database connection"""
    try:
        # # for phpmysql
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
            password='Admin_password_2568',
            database='mydatabase'
        )
        
        return connection
            
    except Error as e:
        print(f"Error: {e}")
        return None


def add_user(first_name, last_name, username, password):
    """Add a user to the 'user' table"""
    connection = create_connection()

    if connection is None:
        print("Unable to connect to the database.")
        raise Exception("Unable to connect to the database.")

    try:
        cursor = connection.cursor()
        insert_query = """
            INSERT INTO "user" ("firstName", "lastName", "username", "password", "TimeStamp")
            VALUES (%s, %s, %s, %s, TIMEZONE('Asia/Bangkok', NOW()))
        """
        cursor.execute(insert_query, (first_name, last_name, username, password))
        connection.commit()
        print("User added successfully!")

    except Error as e:
        connection.rollback()
        print(f"Error: {e}")
        raise Exception(f"Database insert error: {e}")
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")

# def add_user(first_name, last_name, username, password):
#     """Add a user to the 'user' table"""
#     connection = create_connection()

#     if connection is None:
#         print("Unable to connect to the database.")
#         return

#     try:
#         cursor = connection.cursor()

#         # Query to insert new user
#         insert_query = """
#             INSERT INTO "user" (firstName, lastName, username, password)
#             VALUES (%s, %s, %s, %s)
#         """
#         cursor.execute(insert_query, (first_name, last_name, username, password))
        
#         connection.commit()
#         print("User added successfully!")

#     except Error as e:
#         print(f"Error: {e}")
    
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()
#             # print("MySQL connection is closed.")
#             print("postgreSSQL connection is closed.")