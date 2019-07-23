
from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
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
    def list_employees(self):
        self.cur.execute("SELECT name, email FROM employees LIMIT 50")
        result = self.cur.fetchall()
        return result

@app.route("/")
def template():
    return render_template("template.html")
# @app.route('/home')
# def home():
#     return render_template("home.html")

@app.route('/home')
def employees():
    def db_query():
        db = Database()
        emps = db.list_employees()
        return emps
    res = db_query()
    return render_template('employees.html', result=res, content_type='application/json')

@app.route("/about")
def about():
    return render_template("about.html")
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
#	read the posted values from the UI
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']

	_hashed_password = generate_password_hash(_password)
	cursor.callproc('sp_createUser',(_name,_email,_hashed_password))

	data = cursor.fetchall()

	if len(data) is 0:
		conn.commit()
		return json.dumps({'message':'User created successfully !'})
	else:
		return json.dumps({'error':str(data[0])})

if __name__ == "__main__":
    app.run(debug=True)
