from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, current_user
from app.models.user import User
from app.DAO.userDAO import UserDAO

login = Blueprint('login', __name__)
userDAO = UserDAO()

@login.route("/", methods=["GET", "POST"])
def login_usuario():
    
    if current_user.is_authenticated:
        return redirect(url_for('home.homepage'))

    if request.method == "POST":
        email = request.form.get('email')
        senha = request.form.get('senha')

        user = userDAO.buscar_por_email(email)

        if user and user.check_password(senha):
            login_user(user) 
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("home.homepage"))
        else:
            flash("Usuário ou senha inválidos!", "danger")
    return render_template("login.html")

@login.route('/logout')
def logout_usuario():
    logout_user()
    flash(f'Você fez o logout!', category='info')
    return redirect(url_for('login.login_usuario'))
