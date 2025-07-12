from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user
from app.models.user import User
from app.DAO.userDAO import UserDAO

cadastro = Blueprint('cadastro', __name__)
userDAO = UserDAO()

@cadastro.route('/',  methods=["GET", "POST"])
def cadastro_usuario():

    if request.method == "POST":
        email = request.form.get('email')
        senha = request.form.get('senha')
        confirm_senha = request.form.get("confirm_senha")
        nome = request.form.get('nome')

        if senha != confirm_senha:
            flash("Senhas diferentes. Tente novamente.", "warning")
            return redirect(url_for("cadastro.cadastro_usuario"))

        if userDAO.buscar_por_email(email):
            flash("E-mail já cadastrado, tente outro.", "danger")
            return redirect(url_for("cadastro.cadastro_usuario"))
        
        user = User(nome=nome, email=email)
        user.set_password(senha)
        userDAO.criar_usuario(user)
        login_user(user)

        flash(f'Conta criada com sucesso para {nome}!', 'success' )
        return redirect(url_for('home.homepage'))
        
    return render_template('cadastro.html')