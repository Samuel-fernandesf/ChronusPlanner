from app.models.event import Event
from app.utils.db import db

class EventDAO:

    def criar_evento(self, evento):
        db.session.add(evento)
        db.session.commit()
        return evento

    def buscar_por_id(self, id):
        evento = Event.query.filter_by(id=id).first()
        return evento
    
    def buscar_por_usuario(self, id_user):
        evento = Event.query.filter_by(user_id=id_user).all()
        return evento
    
    def editar(self, evento):
        eventoObj = Event.query.filter_by(id=evento['id']).first()

        eventoObj.titulo = evento['titulo']
        eventoObj.descricao = evento['descricao']
        eventoObj.data = evento['data']
        eventoObj.horario_inicio = evento['horario_inicio']
        eventoObj.horario_fim = evento['horario_fim']
    
        db.session.commit()
        return eventoObj

    def excluir(self, id):
       evento = Event.query.filter_by(id=id).first()
       db.session.delete(evento)
       db.session.commit()
       return evento
