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