from utils.db import db

class Event(db.Model):
    __tablename__ = 'event'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500), nullable=True)
    data = db.Column(db.Date, nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    criado_em = db.Column(db.Datetime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    
    def __init__(self, titulo, descricao, data, horario_inicio, horario_fim, criado_em, user_id):
        self.titulo = titulo
        self.descricao = descricao
        self.data = data
        self.horario_inicio = horario_inicio
        self.horario_fim = horario_fim
        self.criado_em = criado_em
        self.user_id = user_id