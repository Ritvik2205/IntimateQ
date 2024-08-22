from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from flask_login import login_required, current_user
from . import db
import uuid
# from .decorators import user_required, doctor_required

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("index.html", user=current_user)


@views.route('/all_doctors')
def doctors():
    return render_template("doctors.html", user=current_user)

@views.route('/doctor_dashboard/<doctor_id>')
@login_required
def doctor_dashboard(doctor_id):
    return render_template("doctor_dashboard.html", user=current_user, doctor_id=doctor_id)

@views.route('/chat/<room_code>')
@login_required
def chat(room_code):
    return render_template("chat.html", user=current_user, room_code=room_code)

rooms = []

@views.route('/generate_room/<doctor_id>', methods=['POST'])
@login_required
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