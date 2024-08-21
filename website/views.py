from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("index.html", user=current_user)


@views.route('/all_doctors')
@login_required
def doctors():
    return render_template("doctors.html", user=current_user)


@views.route('/doctor/<doctor_id>')
@login_required
def doctor_page(doctor_id):
    return render_template("doctor_page.html", user=current_user, doctor_id=doctor_id)