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






print("🔥 routes.py loaded")
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






line_table_mapping = {
    "a1": "calculate_data_a1",
    "a2": "calculate_data_a2",
    "a3": "calculate_data_a3",
    "b7": "calculate_data_b7",
    "b8": "calculate_data_b8",
    "b9": "calculate_data_b9",
    "b10": "calculate_data_b10",
    "b12": "calculate_data_b12",
    "b13": "calculate_data_b13",
    "b16": "calculate_data_b16",
    "b17": "calculate_data_b17",
    "b18": "calculate_data_b18",
    "c1": "calculate_data_c1",
    "c2": "calculate_data_c2",
    "c3": "calculate_data_c3",
    "c4": "calculate_data_c4",
    "c5": "calculate_data_c5",
    "c6": "calculate_data_c6",
    "c7": "calculate_data_c7",
    "c8": "calculate_data_c8",
    "c9": "calculate_data_c9",
    "c10": "calculate_data_c10",
    "c11": "calculate_data_c11",
    "d1": "calculate_data_d1",
    "d2": "calculate_data_d2",
    "d3": "calculate_data_d3",
    "d5": "calculate_data_d5",
    "d6": "calculate_data_d6",
    "d7": "calculate_data_d7",
    "d8": "calculate_data_d8",
    "d9": "calculate_data_d9",
    "d10": "calculate_data_d10",
    "d11": "calculate_data_d11",
    "d12": "calculate_data_d12",
    "d13": "calculate_data_d13",
    "h1": "calculate_data_h1",
    "h2": "calculate_data_h2",
    "h4": "calculate_data_h4",
    "h5": "calculate_data_h5",
    "h6": "calculate_data_h6",
    "h7": "calculate_data_h7",
    "h8": "calculate_data_h8",
    "h9": "calculate_data_h9",
    "h10": "calculate_data_h10",
    "i1": "calculate_data_i1",
    "i2": "calculate_data_i2",
    "i4": "calculate_data_i4",
    "m1": "calculate_data_m1",
    "n1": "calculate_data_n1",
    "o1": "calculate_data_o1",
    "q1": "calculate_data_q1",
    "s1": "calculate_data_s1",
}

@app.route('/api/oee_<line_id>')
def get_latest_oee(line_id):
    table_name = line_table_mapping.get(line_id.lower())

    if not table_name:
        return {"error": f"Invalid line_id '{line_id}'"}, 400

    connection = create_connection()
    if not connection:
        return {"error": "DB connection failed"}, 500

    try:
        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
        row = cursor.fetchone()
        connection.close()

        if row:
            return {
                "OEE": float(row[4]),         # ✅ ส่ง key ชื่อเดียวกันทั้งหมด
                "TimeStamp": str(row[6])
            }
        else:
            return {"OEE": None}
    except Exception as e:
        return {"error": str(e)}, 500











# @app.route('/api/oee_a1')
# def get_latest_A1():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_a1
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_a2')
# def get_latest_A2():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_a2
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_A2": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_A2": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_a3')
# def get_latest_A3():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_a3
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_A3": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_A3": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_b7')
# def get_latest_B7():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_b7
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_B7": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_B7": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_b8')
# def get_latest_B8():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_b8
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_B8": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_B8": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_b9')
# def get_latest_B9():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_b9
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_B9": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_B9": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_b10')
# def get_latest_B10():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_b10
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_B10": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_B10": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_b12')
# def get_latest_B12():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_b12
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_B12": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_B12": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_b13')
# def get_latest_B13():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_b13
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_B13": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_B13": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_b16')
# def get_latest_B16():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_b16
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_B16": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_B16": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_b17')
# def get_latest_B17():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_b17
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_B17": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_B17": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_b18')
# def get_latest_B18():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_b18
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_B18": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_B18": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_c1')
# def get_latest_c1():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_c1
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_C1": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_C1": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_c2')
# def get_latest_c2():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_c2
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_C2": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_C2": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_c3')
# def get_latest_c3():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_c3
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_C3": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_C3": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_c4')
# def get_latest_c4():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_c4
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_C4": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_C4": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_c5')
# def get_latest_c5():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_c5
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_C5": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_C5": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_c6')
# def get_latest_c6():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_c6
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_C6": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_C6": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_c7')
# def get_latest_c7():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_c7
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_C7": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_C7": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_c8')
# def get_latest_c8():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_c8
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_C8": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_C8": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_c9')
# def get_latest_c9():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_c9
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_C9": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_C9": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_c10')
# def get_latest_c10():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_c10
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_C10": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_C10": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500
    
# @app.route('/api/oee_c11')
# def get_latest_c11():
#     connection = create_connection()
#     if not connection:
#         return {"error": "Unable to connect to the database"}, 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             SELECT * FROM calculate_data_c11
#             ORDER BY id DESC
#             LIMIT 1
#         """
#         cursor.execute(query)
#         row = cursor.fetchone()
#         cursor.close()
#         connection.close()

#         if row:
#             return {
#                 "OEE_C11": float(row[4]),  # ✅ ดึงค่าจาก column 'a'
#                 "TimeStamp": str(row[6])
#                 # "Start_Time": str(row[2])
#             }
#         else:
#             return {"OEE_C11": None}
#     except Exception as e:
#         print("Database error:", e)
#         return {"error": str(e)}, 500