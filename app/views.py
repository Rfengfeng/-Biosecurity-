from flask import render_template,flash, request, session, redirect, url_for
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

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

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

@app.route('/dashboard')
def dashboard():
    # Check if user is loggedin
    if 'loggedin' in session:
        if session['role'] == 'RiverUser':
            return render_template('RiverUser_panel.html')
        elif session['role'] == 'staff':
            return redirect(url_for('staff_dashboard'))
        elif session['role'] == 'admin':
            return redirect(url_for('admin_dashboard'))

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
                return redirect(url_for('dashboard'))
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
            return render_template('register.html', msg=msg)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
            return render_template('register.html', msg=msg)
        elif len(password) < 8:
            msg = 'Password must be at least 8 characters long.'
            return render_template('register.html', msg=msg)
        elif not any(char.isdigit() for char in password):
            msg = 'Password must contain at least one digit.'
            return render_template('register.html', msg=msg)
        elif not any(char.islower() for char in password) and not any(char.isupper() for char in password):
            msg = 'Password must contain at least one uppercase or one lowercase letter.'
            return render_template('register.html', msg=msg)
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            return render_template('register.html', msg=msg)
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
            return render_template('register.html', msg=msg)
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = hashing.hash_value(password, salt='abcd')
            cursor.execute('INSERT INTO secureaccount VALUES (NULL, %s, %s, %s, %s)', (username, hashed, email,'RiverUser',))
            connection.commit()
            msg = 'You have successfully registered! Please login!'
        return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


@app.route('/change_psw/<int:user_id>', methods=['GET', 'POST'])
def change_psw(user_id):
    cursor = getCursor()
    cursor.execute('SELECT * FROM secureaccount WHERE id = %s', (user_id,))
    account = cursor.fetchone()
    return render_template('change_pwd.html', user_id=user_id,user=account)

@app.route('/update_psw/<int:user_id>', methods=['GET', 'POST'])
def update_psw(user_id):
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'password' in request.form:
        # Create variables for easy access
        password = request.form['password']
        password2 = request.form['password2']
        # Check if account exists using MySQL
        cursor = getCursor()
        cursor.execute('SELECT * FROM secureaccount WHERE id = %s', (user_id,))
        account = cursor.fetchone()
        # If account not exists show error and validation checks
        if not account:
            msg = 'Account does not exist!'
        elif password != password2:
            msg = '''Passwords don't match each other!''' 
        elif len(password) < 8:
            msg = 'Password must be at least 8 characters long.'
        elif not any(char.isdigit() for char in password):
            msg = 'Password must contain at least one digit.'
        elif not any(char.islower() for char in password) and not any(char.isupper() for char in password):
            msg = 'Password must contain at least one uppercase or one lowercase letter.'

        elif not password or not password2:
            msg = 'Please fill out the form!'
        else:
            # Account does exists and the form data is valid, now update account into accounts table
            hashed = hashing.hash_value(password, salt='abcd')
            cursor = getCursor()
            cursor.execute('UPDATE secureaccount SET password = %s  WHERE id = %s', (hashed, user_id,))
            connection.commit()    
            msg = "Password changed sucessfully!"  
    flash(msg)
    return render_template('change_pwd.html', user_id=user_id,user=account)



@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id, msg=''):
    msg = msg
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        print('look for the user')
        cursor = getCursor()
        cursor.execute('SELECT * FROM secureaccount WHERE id = %s;', (int(user_id),))
        account = cursor.fetchone()

        if account:
            print('user found, id',account[0],'username',account[1],'role',account[4],'user_id',user_id)

        user = {}   
        user['user_id'] = account[0] 
        user['user_name'] = account[1]
        user['password'] = account[2]    
        user['email'] = account[3]   
        user['role'] = account[4]
        user['first_name'] = ''
        user['last_name'] = ''
        user['address'] = ''
        user['phone_number'] = ''
        user['date_joined'] = ''
        user['status'] = ''
        user['staff_number'] = ''
        user['hire_date'] = ''
        user['position'] = ''
        user['department'] = ''
        if user['role'] == 'RiverUser':             
            cursor = getCursor()
            print('SELECT * FROM riveruser WHERE user_id = %s;', (int(user_id),))
            cursor.execute('SELECT * FROM riveruser WHERE user_id = %s;', (int(user_id),))
            account_RU = cursor.fetchone()
            if account_RU:
                print('account found in riveruser',account_RU)
                user['first_name'] = account_RU[1]
                user['last_name'] = account_RU[2]
                user['address'] = account_RU[3]
                user['phone_number'] = account_RU[4]
                user['date_joined'] = account_RU[5]
                user['status'] = account_RU[6]
        if user['role'] == 'staff' or user['role'] == 'admin': 
            cursor.execute('SELECT * FROM staffuser WHERE user_id = %s;', (int(user_id),))
            account_SF = cursor.fetchone()   
            if account_SF:   
                print('account found in staffuser')           
                user['staff_number'] = account_SF[1]  
                user['first_name'] = account_SF[2]
                user['last_name'] = account_SF[3]
                user['address'] = account_SF[4]
                user['phone_number'] = account_SF[5]
                user['hire_date'] = account_SF[6]                   
                user['position'] = account_SF[7]                    
                user['department'] = account_SF[8] 
                user['status'] = account_SF[9]
        # Show the profile page with account info
        return render_template('profile.html', user=user ,msg = msg)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))



@app.route('/update_profile/<int:user_id>', methods=['GET', 'POST'])
def update_profile(user_id):
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' :
        # Check if account exists in secureaccount
        cursor = getCursor()
        cursor.execute('SELECT * FROM secureaccount WHERE id = %s',(int(user_id),))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if not account:
            msg = 'Account does not exist!'
            print(msg)
        else:            
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            address = request.form['address']
            phone_number = request.form['phone_number']
            status = request.form['status']
            # update profile data table
            if account[4] == 'RiverUser':                 
                date_joined = datetime.now().date()
                # Check if account exists in riveruser
                cursor = getCursor()
                cursor.execute('SELECT * FROM riveruser WHERE user_id = %s', (int(user_id),))
                account_RU = cursor.fetchone()
                # If account not exists if riveruser:
                print('create a new profile for riveruser')
                if not account_RU:
                    cursor.execute('''INSERT INTO riveruser (first_name, 
                                           last_name,  
                                           address,  
                                           phone_number,  
                                           date_joined,  
                                           status,  
                                           user_id)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)''', 
                                    (first_name, 
                                        last_name, 
                                        address, 
                                        phone_number, 
                                        date_joined, 
                                        status, 
                                        int(user_id),))
                    connection.commit()

                # If account exists 
                if account_RU:
                    print('update profile for riveruser')
                    cursor.execute('''UPDATE riveruser SET first_name = %s, 
                                last_name = %s,  
                                address = %s,  
                                phone_number = %s,  
                                date_joined = %s,  
                                status = %s
                                WHERE user_id = %s''', 
                                (first_name, 
                                    last_name, 
                                    address, 
                                    phone_number, 
                                    date_joined, 
                                    status, 
                                    int(user_id),))
                    connection.commit()
                msg = 'Suceessfully updated! River user'
                print(msg)
            if account[4] == 'staff' or account[4] == 'admin':                 
                staff_number = request.form['staff_number']
                hire_date = request.form['hire_date']
                position = request.form['position']
                department = request.form['department']    
                #check date format
                if not validate_date(hire_date):
                    msg='date format for hire_date'
                    return redirect(url_for('profile',user_id = account[0],msg = msg))

                # Check if account exists in staffuser
                cursor = getCursor()
                cursor.execute('SELECT * FROM staffuser WHERE user_id = %s', (int(user_id),))
                account_SU = cursor.fetchone()
                # If account not exists if staffuser:
                print('create a new profile for staffuser')
                if not account_SU:
                    cursor.execute('''INSERT INTO staffuser 
                                    (staff_number, first_name, last_name, address, work_phone_number, hire_date, position, department, status, user_id) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                                    (staff_number, first_name, last_name, address, phone_number, hire_date, position, department, status, int(user_id)))
                    connection.commit()


                # If account exists 
                if account_SU:
                    print('updating profile for staffuser')
                    cursor.execute('''UPDATE staffuser SET 
                                staff_number = %s, 
                                first_name = %s, 
                                last_name = %s,  
                                address = %s,  
                                work_phone_number = %s,  
                                hire_date = %s,   
                                position = %s,  
                                department = %s, 
                                status = %s
                                WHERE user_id = %s''', 
                                (staff_number,
                                    first_name, 
                                    last_name, 
                                    address, 
                                    phone_number, 
                                    hire_date, 
                                    position, 
                                    department, 
                                    status, 
                                    int(user_id),))
                    connection.commit()                        
    
            msg = 'Suceessfully updated!'
    print(msg)
    return redirect(url_for('profile',user_id = account[0],msg = msg))


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