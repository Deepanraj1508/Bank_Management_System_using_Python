from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import hashlib
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='templates', static_url_path='/static', static_folder='static')
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a random string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost/Bank_Management'  # Update with your MySQL connection details
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class BankStaff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)  # Increase the length for SHA-256
    gender = db.Column(db.String(10), nullable=False)
    bod = db.Column(db.Date, nullable=False)
    education = db.Column(db.String(20), nullable=False)
    employment_history = db.Column(db.Text, nullable=True)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(10), nullable=False)  # Assuming phone numbers are stored as strings
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
        gender = request.form['gender']
        bod = datetime.strptime(request.form['bod'], '%Y-%m-%d').date()
        education = request.form['education']
        employment_history = request.form.get('employment_history')
        phone = request.form['phone']
        address = request.form['address']
        experience = request.form['experience']

        # Hash the password using SHA-256 with a salt
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

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
            address=address,
            phone=phone,
            experience=experience
        )
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('staff/StaffRegForm.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = BankStaff.query.filter_by(username=username).first()

        if user and user.password == hashlib.sha256(password.encode()).hexdigest():
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('staff/Stafflogin.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('staff/staff_home.html')


#customer page

@app.route('/customerlogin', methods=['GET', 'POST'])
def customerlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = BankStaff.query.filter_by(username=username).first()

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = BankStaff.query.filter_by(username=username).first()

        if user and user.password == hashlib.sha256(password.encode()).hexdigest():
            flash('Logged in successfully!', 'success')
            return redirect(url_for('customerdashboard'))
        else:
            flash('Invalid username or password', 'error')


    return render_template('customer/customerlogin.html')

@app.route('/customerdashboard', methods=['GET', 'POST'])
def customerdashboard():
    return render_template('customer/customerdash.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port='8000')
