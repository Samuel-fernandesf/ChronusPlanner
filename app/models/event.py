from app.utils.db import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = 'event'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500), nullable=True)
    data = db.Column(db.Date, nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __init__(self, titulo, descricao, data, horario_inicio, horario_fim, user_id):
        self.titulo = titulo
        self.descricao = descricao
        self.data = data
        self.horario_inicio = horario_inicio
        self.horario_fim = horario_fim
        self.user_id = user_id