
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
    def employee(self):
        self.cur.execute("SELECT user_name, user_username FROM employee LIMIT 50")
        result = self.cur.fetchall()
        return result

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        details = request.form
        firstName = details['fname']
        lastName = details['lname']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')

@app.route("/")
def template():
    return render_template("template.html")
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/employee')
def employee():
    def db_query():
        db = Database()
        emps = db.employee()
        return emps
    res = db_query()
    print(res)
    return render_template('employee.html', result=res)

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
