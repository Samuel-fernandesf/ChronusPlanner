from app.models.user import User
from app.utils.db import db

class UserDAO:

    def criar_usuario(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def buscar_por_id(self, id):
        user = User.query.filter_by(id=id).first()
        return user
    
    def buscar_por_email(self, email):
        user = User.query.filter_by(email=email).first()
        return user
    
    def editar(self, user):
        userObj = User.query.filter_by(id=user.id).first()

        userObj.nome = user.nome
        db.session.commit()
        return userObj

    def excluir(self, id):
       user = User.query.filter_by(id=id).first()
       db.session.delete(user)
       db.session.commit()
       return user
