from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

home = Blueprint('home', __name__)

@home.route('/')
@login_required
def homepage():
    return render_template('home.html')