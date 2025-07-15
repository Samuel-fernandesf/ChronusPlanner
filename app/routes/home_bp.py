from flask import Blueprint, render_template, redirect, request, url_for, jsonify, flash
from app.models.event import Event
from app.models.task import Task
from app.DAO.taskDAO import TaskDAO
from app.DAO.eventDAO import EventDAO
from app.forms import TaskForm
from app.utils.db import db
from flask_login import login_required, current_user
from datetime import datetime


home = Blueprint('home', __name__)
eventoDAO = EventDAO()
taskDAO = TaskDAO()

@home.route('/')
@login_required
def homepage():
    return render_template('home.html')

@home.route('/calendario')
@login_required
def calendario():
    return render_template('calendar.html')

@home.route('/calendario/api/eventos', methods=['GET', 'POST'])
@login_required
def adicionar_evento():

    #Se for post significa que é para criar um novo evento
    if request.method == 'POST':
        dados = request.json
        try:
            titulo = dados.get('titulo')
            descricao = dados.get('descricao')
            data = dados.get('data')
            horario_inicio = dados.get('horario_inicio')
            horario_fim = dados.get('horario_fim')

            # Converte as datas de strings para time ou date
            data = datetime.strptime(data, '%Y-%m-%d').date() if data else None
            horario_inicio = datetime.strptime(horario_inicio, '%H:%M').time() if horario_inicio else None
            horario_fim = datetime.strptime(horario_fim, '%H:%M').time() if horario_fim else None

            #Validação para o horário de início ser menor que o fim.
            if horario_inicio and horario_fim and horario_inicio >= horario_fim:
                return jsonify({'status': 'error', 'message': 'O horário de início deve ser antes do horário de fim.'}), 400
            
            evento = Event(
                titulo=titulo, 
                descricao=descricao,
                data=data,
                horario_inicio=horario_inicio,
                horario_fim=horario_fim,
                user_id=current_user.id)
            
            eventoDAO.criar_evento(evento)

            # Envia para o front-end que a criação do evento deu certo.
            return jsonify({'status': 'success', 'message': 'Evento criado com sucesso!'}), 201
        
        except Exception as erro:
            return jsonify({'status': 'error', 'message': str(erro)}), 400

    # Serve para listar os eventos em formato json    
    elif request.method == 'GET':
        eventos = eventoDAO.buscar_por_usuario(current_user.id)
        lista = []

        for i in eventos:
            start = f"{i.data.isoformat()}T{i.horario_inicio.strftime('%H:%M:%S')}" if i.horario_inicio else i.data.isoformat()
            end = f"{i.data.isoformat()}T{i.horario_fim.strftime('%H:%M:%S')}" if i.horario_fim else None

            # Cria um dicionário com os dados que o fullcalendar solicita para ver o evento (obrigatórios: title e start)
            evento_json = {
                'id': i.id,
                'title': i.titulo,
                'start': start,
                'descricao': i.descricao,
                'horario_inicio': i.horario_inicio.strftime('%H:%M') if i.horario_inicio else '',
                'horario_fim': i.horario_fim.strftime('%H:%M') if i.horario_fim else '',
                'data': i.data.strftime('%Y-%m-%d')
            }
            if end:
                evento_json['end'] = end

            lista.append(evento_json)

        return jsonify(lista)

@home.route('calendario/api/eventos/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def editar_excluir_evento(id):
    evento = eventoDAO.buscar_por_id(id)

    if not evento or evento.user_id != current_user.id:
        return jsonify({'status': 'error', 'message': 'Evento não encontrado'}), 404
    
    if request.method == 'PUT':
        dados = request.json

        try:
            data = datetime.strptime(dados.get('data'), '%Y-%m-%d').date() if dados.get('data') else None
            inicio = datetime.strptime(dados.get('horario_inicio'), '%H:%M').time() if dados.get('horario_inicio') else None
            fim = datetime.strptime(dados.get('horario_fim'), '%H:%M').time() if dados.get('horario_fim') else None

            novo_evento = {
                'id': evento.id,
                'titulo': dados.get('titulo'),
                'descricao': dados.get('descricao'),
                'data': data,
                'horario_inicio': inicio,
                'horario_fim': fim
            }

            eventoDAO.editar(novo_evento)
            return jsonify({'status': 'success', 'message': 'Evento atualizado com sucesso!'}), 200
        except Exception as erro:
            return jsonify({'status': 'error', 'message': str(erro)}), 400

    elif request.method == 'DELETE':
        try:
            eventoDAO.excluir(id)
            return jsonify({'status': 'success', 'message': 'Evento excluído com sucesso!'}), 200
        except Exception as erro:
            return jsonify({'status': 'error', 'message': str(erro)}), 400

@home.route('/tarefas', methods=['GET', 'POST'])
@login_required
def tarefas():
    form = TaskForm()

    if form.validate_on_submit():
        titulo=form.titulo.data
        descricao=form.descricao.data
        data_limite=form.data_limite.data
        user_id=current_user.id

        nova_task = Task(titulo=titulo, descricao=descricao, data_limite=data_limite, user_id=user_id)
        taskDAO.criar_tarefa(nova_task)

        return redirect(url_for('home.tarefas'))

    tasks = taskDAO.buscar_por_usuario(current_user.id)

    return render_template('tasks.html', form=form, tasks=tasks)

@home.route('/tarefa/<int:id>/concluir', methods=['POST'])
@login_required
def concluir_tarefa(id):
    taskDAO.concluir_tarefa(id)
    return redirect(url_for('home.tarefas'))

@home.route('/tarefa/editar/<int:id>/', methods=['GET', 'POST'])
@login_required
def editar_tarefa(id):
    task = Task.query.get(id)

    form = TaskForm(obj=task)

    if form.validate_on_submit():
        form.populate_obj(task)
        db.session.commit()
        return redirect(url_for('home.tarefas'))
    
    tasks = taskDAO.buscar_por_usuario(current_user.id)

    return render_template('tasks.html', tasks=tasks, task=task, form=form, editar=True)

@home.route('/tarefa/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_tarefa(id):
    taskDAO.excluir(id)
    return redirect(url_for('home.tarefas'))

