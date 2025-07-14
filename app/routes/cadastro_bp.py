from flask import Blueprint, render_template, redirect, url_for, request, flash
from app.forms import Cadastro_Formulario
from app.models.user import User
from app.DAO.userDAO import UserDAO
from flask_login import login_user, logout_user, current_user

cadastro = Blueprint('cadastro', __name__)
userDAO = UserDAO()

@cadastro.route('/',  methods=["GET", "POST"])
def cadastro_usuario():

    form = Cadastro_Formulario()
    if form.validate_on_submit():
        email = form.email.data
        senha = form.senha.data
        confirm_senha = form.confirm_senha.data
        nome = form.nome.data
        
        user = User(nome=nome, email=email)
        user.set_password(senha)
        userDAO.criar_usuario(user)
        login_user(user)

        flash(f'Conta criada com sucesso para {nome}!', 'success' )
        return redirect(url_for('home.homepage'))
        
    return render_template('cadastro.html', form=form)