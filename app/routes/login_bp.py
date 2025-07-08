from flask import Blueprint, render_template, redirect, url_for

login = Blueprint('login', __name__)

@login.route('/')
def login_user():
    return render_template('login.html')