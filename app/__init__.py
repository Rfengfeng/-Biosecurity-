from flask import Flask





app = Flask(__name__, template_folder='../templates',static_folder = '../static')

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'





from app import views
from app import admin_views
from app import staff_views

