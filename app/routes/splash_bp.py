from flask import Blueprint, render_template

splash = Blueprint('splash', __name__)

@splash.route("/")
def splash_screen():
    return render_template("splash.html")
