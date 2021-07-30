from mysql.connector import connect
from flask_mysqldb import MySQL

class Database:
    def __init__(self):
        self.connection = connect(host='127.0.0.1',
                                  database='thesis',
                                  port='3306',
                                  user='root',
                                  password='password')
        self.cursor = self.connection.cursor()
        self.connection.close()

    def connect_database(self):
        self.connection = connect(host='127.0.0.1',
                                  database='thesis',
                                  port='3306',
                                  user='root',
                                  password='password')
        self.cursor = self.connection.cursor()

    #-----writing data to database-------------------------------------------------------------------------------------------------

    def register_user_personal_data(self, first_name, last_name, user_name, user_password, user_role):
        self.connect_database()
        self.cursor.execute("""INSERT INTO application_user (first_name, last_name, user_name, user_password, user_role)
        VALUES (%s, %s, %s, %s, %s, 0);""", (first_name, last_name, user_name, user_password, user_role))
        self.connection.commit()
        result = self.cursor.lastrowid
        self.connection.close()
        return result

    def register_user_skills(self, skill_name, skill_type):
        self.connect_database()
        self.cursor.execute("""INSERT INTO skill (skill_name, skill_type)
        VALUES (%s, %s, 0);""", (skill_name, skill_type))
        self.connection.commit()
        result = self.cursor.lastrowid
        self.connection.close()
        return result

    # post information about new project (to-do) add validation
    def post_project_information(self,
                                 project_title,
                                 project_overview,
                                 project_full_description,
                                 project_if_archived,
                                 project_arcivation_date,
                                 project_author):
        self.connect_database()
        if self.cursor.execute(""" SELECT user_id FROM application_user WHERE user_id = %(project_author)s"""):
            self.cursor.execute("""INSERT INTO project (project_title, project_overview, project_full_description, project_if_archived, project_arcivation_date, project_author)
            VALUES (%s, %s, %s, %s, %s, %s, 0);""", (project_title, project_overview, project_full_description, project_if_archived, project_arcivation_date, project_author))
            self.connection.commit()
            result = self.cursor.lastrowid
            self.connection.close()
            return result
        else:
            return "there is no such user, he/she can not host a project"

    #-----getting data from database-------------------------------------------------------------------------------------------------

    def get_skills(self):
        self.connect_database()
        self.cursor.execute("SELECT skill_name FROM skill ORDER BY skill_type")
        result = self.cursor.fetchall()
        self.connection.close()
        return result

    def get_recommended_projects(self):
        self.connect_database()
        self.cursor.execute("SELECT project_title, project_overview FROM project ORDER BY RAND() LIMIT 3")
        result = self.cursor.fetchall()
        self.connection.close()
        return result

    def get_recommended_users(self):
        self.connect_database()
        self.cursor.execute("SELECT u.user_name, u.user_role, s.skill_name FROM application_user u JOIN skill_user su ON u.user_id = su.user_id JOIN skill s ON s.skill_id = su.skill_id ORDER BY RAND() LIMIT 3");
        result = self.cursor.fetchall()
        self.connection.close()
        return result

    def get_user_name(self):
        self.connect_database()
        self.cursor.execute("SELECT user_name FROM application_user WHERE user_id = 1 ;")
        result = self.cursor.fetchall()
        self.connection.close()
        return result

    def get_user_connections(self):
        self.connect_database()
        self.cursor.execute("SELECT u1.user_name FROM application_user u1 JOIN connection c ON u1.user_id = c.conection_id AND c.user_id = 1 limit 3;")
        result = self.cursor.fetchall()
        self.connection.close()
        return result

    #(TO-DO) application user queries for getting related skills/education history/personal data
    #(TO-DO) dynamically show values from skill table with the following query

