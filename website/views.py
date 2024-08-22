from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from flask_login import login_required, current_user
from . import db
import uuid
from .decorators import user_required, doctor_required
from .models import Doctor
from .auth import get_current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    current_user_info = get_current_user()
    user_type = current_user_info['type']
    return render_template("index.html", user=current_user, user_type=user_type)


@views.route('/all_doctors')
def doctors():
    current_user_info = get_current_user()
    user_type = current_user_info['type']
    return render_template("doctors.html", user=current_user, user_type=user_type)

@views.route('/doctor_dashboard/<doctor_id>')
@doctor_required
def doctor_dashboard(doctor_id):
    current_user_info = get_current_user()
    user_type = current_user_info['type']
    return render_template("doctor_dashboard.html", user=current_user, doctor_id=doctor_id, user_type=user_type)

@views.route('/chat/<room_code>/<doctor_id>')
@login_required
def chat(room_code, doctor_id):
    doctor = Doctor.query.filter_by(doctorID=doctor_id).first()
    current_user_info = get_current_user()
    user_type = current_user_info['type']
    return render_template("chat.html", user=current_user, doctor=doctor, room_code=room_code, user_type=user_type)

rooms = []

@views.route('/generate_room/<doctor_id>', methods=['POST'])
@user_required
def generate_room(doctor_id):
    while True:
        room_code = str(uuid.uuid4())
        if room_code not in rooms:
            # Save room_code to the database if needed
            return jsonify({
                'room_code': room_code,
                'doctor_id':doctor_id
            })
        else:
            continue