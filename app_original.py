from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session


import re
from datetime import datetime
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing


app = Flask(__name__)
hashing = Hashing(app)  #create an instance of hashing

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'


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



@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/redirect_to_index')
def redirect_to_index():
    return redirect(url_for('index'))


# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests
@app.route('/login/', methods=['GET', 'POST'])
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
                # Redirect to home page
                if session['role'] == 'admin':
                    return redirect(url_for('admin_panel'))
                if session['role'] == 'staff':
                    return redirect(url_for('staff_panel'))
                if session['role'] == 'RiverUser':
                    return redirect(url_for('RiverUser'))
                return redirect(url_for('home'))
            else:
                #password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
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
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = hashing.hash_value(password, salt='abcd')
            cursor.execute('INSERT INTO secureaccount VALUES (NULL, %s, %s, %s)', (username, hashed, email,))
            connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        cursor = getCursor()
        cursor.execute('SELECT * FROM secureaccount WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

# http://localhost:5000/logout - this will be the logout page
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))



def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, auth_plugin='mysql_native_password',\
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route('/uploadpanel')
def uploadpanel():
    print("index")
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print("here")
    if request.method == 'POST':
        file = request.files['image']
        print("here")
        if file:
            # Read image data
            image_data = file.read()

            # Store image data as blob in MySQL
            cursor = getCursor()
            cursor.execute('INSERT INTO images (image_data) VALUES (%s)', (image_data,))
            connection.commit()
            print("success")
            return 'File uploaded successfully'
    return 'No file uploaded'

@app.route('/display')
def display_image():
    # Fetch blob data from MySQL
    cursor = getCursor()
    cursor.execute('SELECT image_data FROM images ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()

    # Convert binary blob data to base64 encoding
    image_data_base64 = base64.b64encode(result[0]).decode('utf-8')

    # Pass base64 encoded image data to template
    return render_template('display.html', image_data=image_data_base64)
@app.route('/RiverUser')
def RiverUser():
    current_user={}
    if session['role'] == 'RiverUser':
        current_user['is_authenticated']=session['loggedin'] 
        current_user['userid']=session['id'] 
        current_user['username']=session['username'] 
        current_user['role']=session['role']
        return render_template('RiverUser_panel.html',current_user=current_user)
    
@app.route('/riveruserprofile')
def riveruserprofile():
    return render_template('riveruserprofile.html')

@app.route('/redirect_to_riveruserprofile')
def redirect_to_riveruserprofile():
    return redirect(url_for('riveruserprofile'))

@app.route('/Guide')
def Guide():
    current_user={}
    if session['role'] == 'RiverUser':
        current_user['is_authenticated']=session['loggedin'] 
        current_user['userid']=session['id'] 
        current_user['username']=session['username'] 
        current_user['role']=session['role']
    return render_template('Guide.html',current_user=current_user)
    

@app.route('/redirect_to_Guide')
def redirect_to_Guide():
    return redirect(url_for('Guide'))


@app.route('/staff_panel')
def staff_panel():
    current_user={}
    if session['role'] == 'staff':
        current_user['is_authenticated']=session['loggedin'] 
        current_user['userid']=session['id'] 
        current_user['username']=session['username'] 
        current_user['role']=session['role']
        return render_template('staff_panel.html',current_user=current_user)
    

@app.route('/admin_panel')
def admin_panel():
    current_user={}
    if session['role'] == 'admin':
        current_user['is_authenticated']=session['loggedin'] 
        current_user['userid']=session['id'] 
        current_user['username']=session['username'] 
        current_user['role']=session['role']
        return render_template('admin_panel.html',current_user=current_user)

@app.route('/userprofile_staffadmin')
def userprofile():
    return render_template('userprofile_staffadmin.html')

@app.route('/redirect_to_userprofile_staffadmin')
def redirect_to_userprofile_staffadmin():
    return redirect(url_for('userprofile_staffadmin'))

    
@app.route('/logout')
def logout():
    # 清除会话中的用户信息
    session.pop('username', None)
    # 重定向到登录页面（假设登录页面的路由为'/login'）
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)