from flask import Blueprint, render_template, redirect, url_for

cadastro = Blueprint('cadastro', __name__)

@cadastro.route('/')
def cadastro_user():
    return render_template('cadastro.html')