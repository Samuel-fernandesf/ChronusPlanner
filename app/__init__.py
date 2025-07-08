import os
from flask import Flask
from .routes.cadastro_bp import cadastro
from .routes.login_bp import login
from .routes.home_bp import home
from .utils.db import db

app = Flask(__name__)

#Chaves de Configuração armazenadas em um arquivo .env
app.config['SECRET_KEY'] = 'fa178b6dd2db59558e923a19f479b819e38f5b51933a7ca0c9c3055e76fc5ca9'
caminho = os.path.abspath('app/database/chronus.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{caminho}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Inicializando o banco de dados
db.init_app(app)

#Ligando as rotas ao arquivo principal (registrando)
app.register_blueprint(login)
app.register_blueprint(cadastro, url_prefix='/cadastro')
app.register_blueprint(home, url_prefix='/home')
