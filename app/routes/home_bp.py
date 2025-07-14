from flask import Blueprint, render_template, redirect, request, url_for, jsonify
from app.models.event import Event
from app.DAO.eventDAO import EventDAO
from flask_login import login_required, current_user
from datetime import datetime


home = Blueprint('home', __name__)
eventoDAO = EventDAO()

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

    # Se não é post, logo é get. Serve para listar os eventos em formato json    
    else:
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

@home.route('/tarefas')
@login_required
def tarefas():
    return render_template('tasks.html')

