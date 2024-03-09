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

@app.route("/admin/dashboard")
def admin_dashboard():
    return "Admin Dashboard"

@app.route("/admin/profile")
def admin_profile():
    return "Admin Profile"



@app.route('/admin/edit_pest/<int:pest_id>')
def edit_pest(pest_id):    
    # get a specific guide using MySQL
    cursor = getCursor()
    cursor.execute("SELECT * FROM freshwater_guide WHERE freshwater_id = %s", (pest_id,))
    pest = cursor.fetchone()
    cursor.close()

    pest = list(pest)
    # Convert binary blob data to base64 encoding
    if pest[8]:
        pest[8] = base64.b64encode(pest[8]).decode('utf-8')
    return render_template('edit_pest_details.html', pest=pest)
       

@app.route('/admin/delete_pest/<int:pest_id>')
def delete_pest(pest_id):    
    # Delete a specific pest from the database using MySQL
    cursor = getCursor()
    cursor.execute("DELETE FROM freshwater_guide WHERE freshwater_id = %s", (pest_id,))
    connection.commit()
    cursor.close()

    return redirect(url_for('homepage'))


@app.route("/admin/add_pest")
def add_pest():
    return render_template('add_pest.html')

@app.route("/admin/add_pest_into_database", methods=['POST'])
def add_pest_into_sql():  
    if request.method == 'POST':
        pest_image = request.files.get('pest_image')
        if pest_image:
            # Read image data
            image_data = pest_image.read()
        pest_type = request.form['pest_type']
        in_nz = request.form['in_nz']
        common_name = request.form['common_name']
        scientific_name = request.form['scientific_name']
        key_characteristics = request.form['key_characteristics']
        biology_description = request.form['biology_description']
        impacts = request.form['impacts']

        # Store image data as blob in MySQL
        cursor = getCursor()
        # 准备SQL语句
        sql = """INSERT INTO freshwater_guide (freshwater_item_type, present_in_NZ, common_name, scientific_name, 
                                                key_characteristics, biology_description, impacts, primary_image) 
                VALUES (%(pest_type)s, %(in_nz)s, %(common_name)s, %(scientific_name)s, %(key_characteristics)s, 
                        %(biology_description)s, %(impacts)s, %(image_data)s)"""

        # 执行新增操作
        cursor.execute(sql, {'pest_type': pest_type, 'in_nz': in_nz, 'common_name': common_name, 'scientific_name': scientific_name,
                            'key_characteristics': key_characteristics, 'biology_description': biology_description, 
                            'impacts': impacts, 'image_data': image_data})

        
        connection.commit()
        msg = 'File uploaded successfully'
        return redirect(url_for('homepage'))
    else:
        return ("Method Not Allowed")

@app.route("/admin/update_pest/<int:pest_id>", methods=['POST'])
def update_pest(pest_id):    
    if request.method == 'POST':
        pest_image = request.files.get('pest_image')
        if pest_image:
            # Read image data
            image_data = pest_image.read()
        pest_type = request.form['pest_type']
        in_nz = request.form['in_nz']
        common_name = request.form['common_name']
        scientific_name = request.form['scientific_name']
        key_characteristics = request.form['key_characteristics']
        biology_description = request.form['biology_description']
        impacts = request.form['impacts']

        # Store image data as blob in MySQL
        cursor = getCursor()
        # 准备SQL语句
        sql = """UPDATE freshwater_guide
                SET freshwater_item_type = %(pest_type)s, present_in_NZ = %(in_nz)s, common_name = %(common_name)s, scientific_name = %(scientific_name)s,
                    key_characteristics = %(key_characteristics)s, biology_description = %(biology_description)s, impacts = %(impacts)s,
                    primary_image = %(image_data)s
                WHERE freshwater_id = %(pest_id)s"""

        # 执行更新操作
        cursor.execute(sql, {'pest_type': pest_type, 'in_nz': in_nz, 'common_name': common_name, 'scientific_name': scientific_name,
                             'key_characteristics': key_characteristics, 'biology_description': biology_description, 'impacts': impacts,
                             'image_data': image_data, 'pest_id': pest_id})
        
        connection.commit()
        msg = 'File uploaded successfully'
        return redirect(url_for('homepage'))
    else:
        return ("Method Not Allowed")

