from app import app
from flask import render_template, request, session, redirect, url_for

@app.route("/staff/dashboard")
def staff_dashboard():
    return render_template('staff_panel.html')

