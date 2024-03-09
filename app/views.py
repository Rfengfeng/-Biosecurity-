from flask import render_template, request, session, redirect, url_for
from app.functions import image_type

import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing
import base64
from app import app

from flask_hashing import Hashing


hashing = Hashing(app)  #create an instance of hashing

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, auth_plugin='mysql_native_password',\
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn


# # 自定义装饰器函数，用于检查用户是否已登录
# def login_required(func):
#     def wrapper(*args, **kwargs):
#         if 'user_id' not in session:
#             return redirect(url_for('login'))
#         return func(*args, **kwargs)
#     return wrapper

@app.route('/')
def homepage():
    # get a list of all guide using MySQL
    cursor = getCursor()
    cursor.execute("SELECT * FROM freshwater_guide")  
    pests = cursor.fetchall()
    cursor.close()
    return render_template('homepage.html',allpests=pests)

@app.route('/pests/<int:pest_id>/details')
def view_pest(pest_id): 
    # get a specific guide using MySQL
    cursor = getCursor()
    cursor.execute("SELECT * FROM freshwater_guide WHERE freshwater_id = %s", (pest_id,))
    pest = cursor.fetchone()
    # Convert binary blob data to base64 encoding
    pest = list(pest)
    if  pest[8]:
        pest[8] = base64.b64encode(pest[8]).decode('utf-8')
    cursor.close()
    return render_template('view_pest.html', pest=pest)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']
        # Check if account exists using MySQL
        cursor = getCursor()
        cursor.execute('SELECT * FROM secureaccount WHERE username = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account is not None:
            password = account[2]
            if hashing.check_value(password, user_password, salt='abcd'):
            # If account exists in accounts table 
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account[0]
                session['username'] = account[1]
                session['role'] = account[4]
                return redirect(url_for('homepage'))
                # Redirect to home page
                # if session['role'] == 'admin':
                #     return redirect(url_for('admin_panel'))
                # if session['role'] == 'staff':
                #     return redirect(url_for('staff_panel'))
                # if session['role'] == 'RiverUser':
                #     return redirect(url_for('RiverUser'))
            else:
                #password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'
    return render_template('login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = getCursor()
        cursor.execute('SELECT * FROM secureaccount WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$', password):
            msg = 'Password must be at least 8 characters long and have a mix of character types.'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = hashing.hash_value(password, salt='abcd')
            cursor.execute('INSERT INTO secureaccount VALUES (NULL, %s, %s, %s)', (username, hashed, email,))
            connection.commit()
            msg = 'You have successfully registered! Please login!'
        return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = getCursor()
        cursor.execute('SELECT * FROM secureaccount WHERE id = %s;', (int(user_id),))
        account = cursor.fetchone()

        user = {}        
        if session['role'] == 'RiverUser': 
            cursor.execute('SELECT * FROM riveruser WHERE user_id = %s;', (int(user_id),))
            account_RU = cursor.fetchone()
            user['user_id'] = account_RU[0]
            user['first_name'] = account_RU[1]
            user['last_name'] = account_RU[2]
            user['address'] = account_RU[3]
            user['email'] = account[3]
            user['phone_number'] = account_RU[5]
            user['date_joined'] = account_RU[6]
            user['status'] = account_RU[7]
        if session['role'] == 'staff' or session['role'] == 'admin': 
            cursor.execute('SELECT * FROM staffuser WHERE user_id = %s;', (int(user_id),))
            account_SF = cursor.fetchone()             
            user['user_id'] = account_SF[0]                  
            user['staff_number'] = account_SF[1]  
            user['first_name'] = account_SF[2]
            user['last_name'] = account_SF[3]
            user['address'] = account_SF[4]
            user['email'] = account[3]
            user['phone_number'] = account_SF[5]
            user['hire_date'] = account_SF[6]                   
            user['position'] = account_SF[7]                    
            user['department'] = account_SF[8] 
            user['status'] = account_SF[9]
        # Show the profile page with account info
        return render_template('profile.html', user=user, account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/user_list')
def user_list():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = getCursor()
        cursor.execute('SELECT * FROM secureaccount ;')
        accounts = cursor.fetchall()
    return render_template('user_list.html', users=accounts)


@app.route('/logout')
def logout():
    # 清除会话中的用户标识信息，实现登出功能
    session.pop('id', None)
    return redirect(url_for('homepage'))