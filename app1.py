from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__, template_folder='templates', static_url_path='/static', static_folder='static')
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random string
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class BankStaff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    bod = db.Column(db.Date, nullable=False)
    education = db.Column(db.String(20), nullable=False)
    employment_history = db.Column(db.Text, nullable=True)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.Integer, nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')


#Staff Page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        gender = request.form['gender'] # Get the string representation of the date
        bod_str = request.form['bod']  # Get the string representation of the date
        bod = datetime.strptime(bod_str, '%Y-%m-%d').date() 
        education = request.form['education']
        employment_history = request.form.get('employment_history')
        phone = request.form.get('phone')# Use get to handle potential absence
        address = request.form['address']
        experience = request.form['experience']

        hashed_password = generate_password_hash(password)

        new_user = BankStaff(
            fname=fname,
            lname=lname,
            email=email,
            username=username,
            password=hashed_password,
            gender=gender,
            bod=bod,
            education=education,
            employment_history=employment_history,
            phone=phone,
            address=address,
            experience=experience,
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('auth/StaffRegForm.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = BankStaff.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('auth/Stafflogin.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('auth/staff_home.html')


#customer page

@app.route('/customerlogin', methods=['GET', 'POST'])
def customerlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = BankStaff.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            flash('Logged in successfully!', 'success')
            return redirect(url_for('customerdashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('auth/customerlogin.html')

@app.route('/customerdashboard', methods=['GET', 'POST'])
def customerdashboard():
    return render_template('auth/customerdash.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port='8000')