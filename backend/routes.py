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
import mysql.connector
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
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM user WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user and bcrypt.check_password_hash(user['password'], password_input):
                # เก็บข้อมูล user ใน session
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash("Login successful!", "success")
                return redirect(url_for('home'))
            else:
                flash("Invalid username or password", "danger")

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
            flash(f"Registration failed: {str(e)}", "danger")

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()  # ล้าง session ทั้งหมด
    flash("You have been logged out.", "info")
    return redirect(url_for('index'))