from flask import Flask, render_template, request, redirect
from utils.database import Database
from flask_mysqldb import MySQL
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
database = Database()


@app.route('/')
def index():
    return 'This is index'

@app.route('/user_registration', methods=['GET', 'POST'])
def user_registration():
    skill_data = database.get_skills()
    return render_template("registration_form.html", skill_data=skill_data)
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        user_name = request.form['user_name']
        user_password = request.form['user_password']
        user_role = request.form['user_role']
        database.register_user(first_name, last_name, user_name, user_password, user_role)
    return redirect('main_page.html')

@app.route('/project_form', methods=['GET', 'POST'])
def post_new_project():
    skill_data = database.get_skills()
    return render_template("project_form.html", skill_data=skill_data)

@app.route('/main_page', methods=['GET', 'POST'])
def main_page():
    user_name_data = database.get_user_name()
    connection_data = database.get_user_connections()
    project_data = database.get_recommended_projects()
    user_data = database.get_recommended_users()
    return render_template('main_page.html', user_name_data=user_name_data, connection_data=connection_data, project_data=project_data, user_data=user_data)


app.run()
