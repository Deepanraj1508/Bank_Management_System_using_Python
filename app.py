from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import event 
import hashlib
from flask_bcrypt import Bcrypt
import random

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


@app.route('/stafflogin', methods=['GET', 'POST'])
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

    return render_template('staff/stafflogin.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('staff/staff_home.html')


#customer page


class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, unique=True)
    password = db.Column(db.String(64), nullable=False)
    password1 =db.Column(db.String(64), nullable=False)
    account_number = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(100))
    dob = db.Column(db.Date)
    mobile = db.Column(db.String(10))
    email = db.Column(db.String(100))
    permanent_address = db.Column(db.String(255))
    state = db.Column(db.String(100))
    city = db.Column(db.String(100))
    pincode = db.Column(db.String(10))
    gender = db.Column(db.String(10))
    blood_group = db.Column(db.String(5))
    identification_type = db.Column(db.String(20))
    identification_number = db.Column(db.String(50))
    education = db.Column(db.String(50))
    differently_abled = db.Column(db.String(3))
    branch_location = db.Column(db.String(100))
    initial_deposit_amount = db.Column(db.Float)
    account_type = db.Column(db.String(20))
    debit_card = db.Column(db.String(3))
    credit_card = db.Column(db.String(3))
    online_banking = db.Column(db.String(3))
    father_name = db.Column(db.String(100))
    mother_name = db.Column(db.String(100))
    emergency_mobile = db.Column(db.String(10))
    emergency_address = db.Column(db.String(255))
    emergency_email = db.Column(db.String(100))
    emergency_state = db.Column(db.String(100))
    emergency_city = db.Column(db.String(100))
    emergency_pincode = db.Column(db.String(10))

def generate_account_number():
    # Generate a random 4-digit number
    random_part = random.randint(1000, 9999)
    # Concatenate the static part (first 7 digits) with the random part (last 4 digits)
    account_number = "95300000" + str(random_part)
    return account_number

def generate_user_id():
    return random.randint(300000, 400000   )
# Event listener to generate account number before inserting a new row
@event.listens_for(FormData, 'before_insert')
def before_insert_generate_account_number(mapper, connection, target):
    target.account_number = generate_account_number()
    
    
@event.listens_for(FormData, 'before_insert')
def before_insert_generate_user_id(mapper, connection, target):
    target.userid = generate_user_id()



# Route for displaying and processing form steps
@app.route('/customer_registration', methods=['GET', 'POST'])
def customer_registration():
    if request.method == 'POST':
        try:
            # Convert initial_deposit_amount to float
            initial_deposit_amount = float(request.form['initial'])

        
            dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()

            # Process form data and store in the database
            form_data = FormData(
                name=request.form['name'],
                dob=dob,
                mobile=request.form['mob1'],
                email=request.form['email1'],
                permanent_address=request.form['add1'],
                state=request.form['state'],
                city=request.form['city'],
                pincode=request.form['pincode'],
                gender=request.form['gender'],
                blood_group=request.form['blood'],
                identification_type=request.form['identification'],
                identification_number=request.form['id'],
                education=request.form['education'],
                differently_abled=request.form['differently_abled'],
                branch_location=request.form['branch'],
                initial_deposit_amount=request.form['initial'],
                account_type=request.form['account_type'],
                debit_card=request.form['debit_card'],
                credit_card=request.form['credit_card'],
                online_banking=request.form['online_banking'],
                father_name=request.form.get('fname', ''),
                mother_name=request.form.get('mname', ''),
                emergency_mobile=request.form.get('mob1', ''),
                emergency_address=request.form.get('add1', ''),
                emergency_email=request.form.get('email1', ''),
                emergency_state=request.form.get('state1', ''),
                emergency_city=request.form.get('city1', ''),
                emergency_pincode=request.form.get('pincode1', ''),
                password=request.form['pass1'],
                password1=request.form['pass2'],
            )
            db.session.add(form_data)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('customerlogin'))
        except ValueError:
            # Handle error if initial_deposit_amount cannot be converted to float
            return "Invalid initial deposit amount. Please enter a valid number."
    return render_template('customer/customerregform.html')


@app.route('/customerlogin', methods=['GET', 'POST'])
def customerlogin():
    if request.method == 'POST':
        userid = request.form['username']
        password = request.form['password']

        # Query the database for the user
        user = FormData.query.filter_by(userid=userid, password=password).first()

        if user:
            # If user exists and password matches, log in
            flash('Logged in successfully!', 'success')
            return redirect(url_for('customerdashboard'))
        else:
            # If login fails, show error message
            flash('Invalid username or password', 'error')

    # Render the login page template
    return render_template('customer/customerlogin.html')

@app.route('/customerdashboard', methods=['GET', 'POST'])
def customerdashboard():
    return render_template('customer/customerdash.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port='8005')
