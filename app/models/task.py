from app.utils.db import db
from datetime import datetime

class Task(db.Model):
    __tablename__ = 'task'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500), nullable=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data_limite = db.Column(db.Date, nullable=False)   
    concluido = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, titulo, descricao, data_limite, user_id):
        self.titulo = titulo
        self.descricao = descricao
        self.criado_em = datetime.utcnow()
        self.data_limite = data_limite
        self.user_id = user_id