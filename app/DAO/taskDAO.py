from app.models.task import Task
from app.utils.db import db

class TaskDAO:

    def criar_tarefa(self, task):
        db.session.add(task)
        db.session.commit()
        return task

    def buscar_por_id(self, id):
        task = Task.query.filter_by(id=id).first()
        return task
    
    def buscar_por_usuario(self, id_user):
        task = Task.query.filter_by(user_id=id_user).order_by(Task.data_limite).all()
        return task
    
    def concluir_tarefa(self, id):
        task = Task.query.get(id)
        task.concluido = True
        db.session.commit()
    
    def excluir(self, id):
       task = Task.query.filter_by(id=id).first()
       db.session.delete(task)
       db.session.commit()
       return task
