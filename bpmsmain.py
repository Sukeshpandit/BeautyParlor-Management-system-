from logging import NullHandler
from flask import Flask,render_template,request,redirect,url_for,session
from flask_login import LoginManager,login_required,logout_user,login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

local_server = True
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bpms'
db=SQLAlchemy(app)
app.secret_key = 'sukeshpandit'

# to get unique user access
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# creatring a database tables
class Users(db.Model,UserMixin):#Test is the table name i given in sql (1st lettaer should be capital) otherthan that everything ids default
    id = db.Column(db.Integer,primary_key=True)#every coloum in DB should be called here
    email = db.Column(db.String(50),unique = True)
    username = db.Column(db.String(50))
    password = db.column(db.String(100))

# creatring a appointment tables
class Appointments(db.Model,UserMixin):#Test is the table name i given in sql (1st lettaer should be capital) otherthan that everything ids default
    aid = db.Column(db.Integer,primary_key=True)#every coloum in DB should be called here
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    services = db.Column(db.String(100))
    date = db.Column(db.String(50),nullable = False)
    time = db.Column(db.String(50),nullable = False)
    phone = db.column(db.String(10))

@app.route('/') #landing page 
def landing_page():
    return render_template('landing_page.html')


@app.route('/signup' , methods=['POST','GET']) #sign up
def signup_page():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(email = email).first() #we will check both email variable above and email in DB is same
        
        if user: #checking if user is already exists
            return render_template('/signup.html')

        new_user = db.engine.execute(f"INSERT INTO `users` (`email`,`username`,`password`) VALUES('{email}','{username}','{password}')")
        return render_template('login.html')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login Form"""
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form['password']
        
        user = Users.query.filter_by(email = email ).first()
        if user is not None:
            session['logged_in'] = True
            return redirect(url_for('main_page'))
        else:
            return render_template('signup.html')
        
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('landing_page.html')


@app.route('/main') #main page 
def main_page():
    return render_template('mainpage.html')#username = current_user.username
   
@app.route('/makeupservices',methods=['POST','GET']) #main page 
def makeupservices_page():
    if request.method == 'POST':
        name =request.form.get('name')
        email = request.form.get('email')
        services = request.form.get('services')
        date = request.form.get('date')
        time = request.form.get('time')
        phone = request.form.get('phone')

        query = db.engine.execute(f"INSERT INTO `appointments` (`name`,`email`,`services`,`date`,`time`,`phone`) VALUES('{name}','{email}','{services}','{date}','{time}','{phone}')")

    return render_template('makeupservices.html')

@app.route('/hairservices',methods=['POST','GET']) #main page 
def hairservices_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        services = request.form.get('services')
        date = request.form.get('date')
        time = request.form.get('time')
        phone = request.form.get('phone')
        query = db.engine.execute(f"INSERT INTO `appointments` (`name`,`email`,`services`,`date`,`time`,`phone`) VALUES('{name}','{email}','{services}','{date}','{time}','{phone}')")

    return render_template('hairservices.html')

@app.route('/bookings')
def bookings(): 
    return render_template('bookings.html')    

app.run(debug=True)


