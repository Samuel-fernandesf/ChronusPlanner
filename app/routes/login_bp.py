from flask import render_template, request, redirect, url_for, flash, Blueprint, current_app
from flask_login import login_user
from app.DAO.userDAO import UserDAO

login = Blueprint('login', __name__)

from flask_login import login_user  # Agora essa função será usada corretamente

@login.route("/", methods=["GET", "POST"])
def login_view():  # 👈 nome diferente de login_user!
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = UserDAO.get_user_by_email(email)

        if user and user.check_password(password):
            login_user(user) 
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("home.homepage"))
        else:
            flash("Credenciais inválidas.", "danger")

    return render_template("login.html")


@login.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["nome"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            flash("As senhas não coincidem.", "warning")
            return redirect(url_for("login.register"))

        # Verifica se já existe usuário
        if UserDAO.get_user_by_email(email):
            flash("Este e-mail já está cadastrado.", "danger")
            return redirect(url_for("login.register"))

        UserDAO.create_user(username, email, password)
        flash("Cadastro realizado com sucesso! Faça o login.", "success")
        return redirect('/')

    return render_template("register.html")




