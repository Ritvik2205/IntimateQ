from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Doctor
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
import pickle
# from .decorators import user_required, doctor_required

auth = Blueprint('auth', __name__)

def get_current_user():
    user = session.get('user')
    if user:
        user_data = pickle.loads(user)
        user_obj = User.query.get(user_data.id)
        if user_obj:
            return int(user_obj.id)
    return None

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                user_json = pickle.dumps(user)
                session['user'] = user_json
                return redirect(url_for('views.doctors'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route("/doctor_login", methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        doctor = Doctor.query.filter_by(email=email).first()
        if doctor:
            if check_password_hash(doctor.password, password):
                flash('Logged in successfully!', category='success')
                login_user(doctor, remember=True)
                doctor_json = pickle.dumps(doctor)
                session['doctor'] = doctor_json
                return redirect(url_for('views.doctors_dashboard'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("doctor_login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    if session.get('user'):
        session.pop('user', None)   
    elif session.get('doctor'):
        session.pop('doctor', None)
    return redirect(url_for('views.home'))

@auth.route("/register", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':        
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        dateOfBirth = request.form.get('date-of-birth')
        gender = request.form.get('gender')

        # if not username or not password:
        #     print('Username and password are required.')
        #     return redirect(url_for('auth.signup'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.', category='error')
        else:
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                dateOfBirth=datetime.strptime(dateOfBirth, '%Y-%m-%d'),
                gender=gender
            )
            db.session.add(new_user)
            db.session.commit()
            # login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))
    else:
        return render_template("register.html", user=current_user)