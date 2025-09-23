# from flask import render_template, request, redirect, url_for
# from backend import app, bcrypt
# import mysql.connector
# from backend.db_utils import add_user

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/home')
# def home():
#     return render_template('home.html')

# @app.route('/example')
# def example():
#     return render_template('example.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

# @app.route('/login')
# def login():
#     return render_template('login.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         first_name = request.form['firstName']
#         last_name = request.form['lastName']
#         username = request.form['username']
#         password = request.form['password']
#         confirm_password = request.form['confirm_password']

#         if password != confirm_password:
#             return "Passwords do not match!"

#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

#         try:
#             # ใช้ฟังก์ชัน add_user ใน db_utils.py เพื่อเพิ่มข้อมูล
#             add_user(first_name, last_name, username, hashed_password)
#             return redirect(url_for('login'))
#         except Exception as e:
#             return f"Registration failed: {str(e)}"

#     return render_template('register.html')







from flask import render_template, request, redirect, url_for, session, flash
from backend import app, bcrypt

# # for phpmysql
# import mysql.connector

# for postgreSQL
import psycopg2
from psycopg2 import Error, extras

from backend.db_utils import create_connection, add_user


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    # เช็คก่อนว่าล็อกอินแล้วหรือยัง
    if 'user_id' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        connection = create_connection()
        if connection:
            try:
                # # syntax of phpmysql
                # cursor = connection.cursor(dictionary=True)
                # query = "SELECT * FROM user WHERE username = %s"
                
                # syntax of postgreSQL
                cursor = connection.cursor(cursor_factory=extras.DictCursor)
                # publish.uer is more specify user
                query = "SELECT * FROM public.user WHERE username = %s"
                
                cursor.execute(query, (username,))
                user = cursor.fetchone()
                
                ## not use this because use finally instead, so use finally is more good
                # cursor.close()
                # connection.close()

                if user and bcrypt.check_password_hash(user['password'], password_input):
                    # เก็บข้อมูล user ใน session
                    session['user_id'] = user['id']
                    session['username'] = user['username']
                    flash("Login successful!", "success")
                    return redirect(url_for('home'))
                else:
                    flash("Invalid username or password", "danger")
            # Exception for check every Error
            # except Exception as e:
            #     flash(f"Database error: {e}", "danger")
            
            # Exception for check Error about database
            except Error as e:
                flash(f"Database error: {e}", "danger")  
            
            # finally for closed the door of database every time when connect database for security         
            finally:
                if connection:
                    cursor.close()
                    connection.close()
        else:
            flash("Unable to connect to the database.", "danger")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            add_user(first_name, last_name, username, hashed_password)
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            print("Register Error:", str(e))  # <== เพิ่มตรงนี้
            flash(f"Registration failed: {str(e)}", "danger")

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()  # ล้าง session ทั้งหมด
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))


@app.route('/api/oee_a1')
def get_latest_A1():
    connection = create_connection()
    if not connection:
        return {"error": "Unable to connect to the database"}, 500

    try:
        cursor = connection.cursor()
        query = """
            SELECT * FROM calculate_data_a1
            ORDER BY id DESC
            LIMIT 1
        """
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row:
            return {
                "OEE": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
                "TimeStamp": str(row[6])
                # "Start_Time": str(row[2])
            }
        else:
            return {"OEE": None}
    except Exception as e:
        print("Database error:", e)
        return {"error": str(e)}, 500
    
@app.route('/api/oee_a2')
def get_latest_A2():
    connection = create_connection()
    if not connection:
        return {"error": "Unable to connect to the database"}, 500

    try:
        cursor = connection.cursor()
        query = """
            SELECT * FROM calculate_data_a2
            ORDER BY id DESC
            LIMIT 1
        """
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row:
            return {
                "OEE_A2": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
                "TimeStamp": str(row[6])
                # "Start_Time": str(row[2])
            }
        else:
            return {"OEE_A2": None}
    except Exception as e:
        print("Database error:", e)
        return {"error": str(e)}, 500
    
@app.route('/api/oee_a3')
def get_latest_A3():
    connection = create_connection()
    if not connection:
        return {"error": "Unable to connect to the database"}, 500

    try:
        cursor = connection.cursor()
        query = """
            SELECT * FROM calculate_data_a3
            ORDER BY id DESC
            LIMIT 1
        """
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row:
            return {
                "OEE_A3": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
                "TimeStamp": str(row[6])
                # "Start_Time": str(row[2])
            }
        else:
            return {"OEE_A3": None}
    except Exception as e:
        print("Database error:", e)
        return {"error": str(e)}, 500
    
@app.route('/api/oee_b7')
def get_latest_B7():
    connection = create_connection()
    if not connection:
        return {"error": "Unable to connect to the database"}, 500

    try:
        cursor = connection.cursor()
        query = """
            SELECT * FROM calculate_data_b7
            ORDER BY id DESC
            LIMIT 1
        """
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row:
            return {
                "OEE_B7": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
                "TimeStamp": str(row[6])
                # "Start_Time": str(row[2])
            }
        else:
            return {"OEE_B7": None}
    except Exception as e:
        print("Database error:", e)
        return {"error": str(e)}, 500
    
@app.route('/api/oee_b8')
def get_latest_B8():
    connection = create_connection()
    if not connection:
        return {"error": "Unable to connect to the database"}, 500

    try:
        cursor = connection.cursor()
        query = """
            SELECT * FROM calculate_data_b8
            ORDER BY id DESC
            LIMIT 1
        """
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row:
            return {
                "OEE_B8": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
                "TimeStamp": str(row[6])
                # "Start_Time": str(row[2])
            }
        else:
            return {"OEE_B8": None}
    except Exception as e:
        print("Database error:", e)
        return {"error": str(e)}, 500
    
@app.route('/api/oee_b9')
def get_latest_B9():
    connection = create_connection()
    if not connection:
        return {"error": "Unable to connect to the database"}, 500

    try:
        cursor = connection.cursor()
        query = """
            SELECT * FROM calculate_data_b9
            ORDER BY id DESC
            LIMIT 1
        """
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row:
            return {
                "OEE_B9": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
                "TimeStamp": str(row[6])
                # "Start_Time": str(row[2])
            }
        else:
            return {"OEE_B9": None}
    except Exception as e:
        print("Database error:", e)
        return {"error": str(e)}, 500
    
@app.route('/api/oee_b10')
def get_latest_B10():
    connection = create_connection()
    if not connection:
        return {"error": "Unable to connect to the database"}, 500

    try:
        cursor = connection.cursor()
        query = """
            SELECT * FROM calculate_data_b10
            ORDER BY id DESC
            LIMIT 1
        """
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        connection.close()

        if row:
            return {
                "OEE_B10": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
                "TimeStamp": str(row[6])
                # "Start_Time": str(row[2])
            }
        else:
            return {"OEE_B10": None}
    except Exception as e:
        print("Database error:", e)
        return {"error": str(e)}, 500