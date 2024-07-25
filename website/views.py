from flask import Blueprint, render_template, jsonify, request, redirect, url_for, session

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("index.html")