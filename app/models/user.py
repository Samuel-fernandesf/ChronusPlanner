from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.utils.db import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), unique=True, nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_crip = db.Column(db.String(128), nullable=False)


    def set_password(self, senha):
        self.senha_crip = generate_password_hash(senha)

    def check_password(self, senha):
        return check_password_hash(self.senha_crip, senha)
