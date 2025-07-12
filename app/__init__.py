import os
from flask import Flask
from .routes.cadastro_bp import cadastro
from .routes.login_bp import login
from .routes.home_bp import home
from .utils.extensions import login_manager
from .utils.db import db
from .models.user import User

# Instância principal da aplicação
app = Flask(__name__)

# Chave secreta e configuração do banco
app.config['SECRET_KEY'] = 'fa178b6dd2db59558e923a19f479b819e38f5b51933a7ca0c9c3055e76fc5ca9'
caminho = os.path.abspath('app/database/chronus.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{caminho}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco de dados
db.init_app(app)

# Inicializando extensão
login_manager.init_app(app)

# Redirecionamento padrão se o usuário não estiver logado
login_manager.login_view = "login.login_usuario"
login_manager.login_message = 'Por favor, realize o login!'
login_manager.login_message_category = 'danger'

# Callback para carregar o usuário logado
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registro dos blueprints (rotas)
app.register_blueprint(login)
app.register_blueprint(cadastro, url_prefix='/cadastro')
app.register_blueprint(home, url_prefix='/home')
