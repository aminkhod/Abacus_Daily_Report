from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL as MySQL
from werkzeug import generate_password_hash, check_password_hash
import pymysql

app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'Abacus_Report'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()

class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = ""
        db = "Abacus_Report"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
    def employee(self):
        self.cur.execute("SELECT user_name, user_username FROM employee LIMIT 50")
        result = self.cur.fetchall()
        return result

@app.route('/')
def employee():
    def db_query():
        db = Database()
        emps = db.employee()
        return emps
    res = db_query()
    print(res)
    return render_template('employee.html', result=res)
if __name__ == "__main__":
    app.run(debug=True)
