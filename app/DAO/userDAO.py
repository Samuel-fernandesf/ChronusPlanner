from app.utils.db import db
from app.models.user import User

class UserDAO:

    @staticmethod
    def create_user(nome, email, password):
        user = User(nome=nome, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
