document.addEventListener('DOMContentLoaded', function() {

    let eventoSelecionado = null //guarda os dados do evento clicado
    let modoEdicao = false
    var modalEventoEl = document.getElementById('staticBackdrop');

    // Cria uma instância do modal do Bootstrap a partir do elemento selecionado, permite abrir, fechar e controlar o modal pelo JS
    var modalEvento = new bootstrap.Modal(modalEventoEl);

    //Abre o modal e preenche a data do evento com a data selecionada
    function abrirModalCriarEvento(dataSelecionada) {
        document.getElementById('data').value = dataSelecionada;
        document.getElementById('titulo').value = '';
        document.getElementById('descricao').value = '';
        document.getElementById('horario_inicio').value = '';
        document.getElementById('horario_fim').value = '';

        modoEdicao = false
        modalEvento.show();
        }

    // pega o ID do botão novo evento e chama uma função que pega a data atual
    document.getElementById('btnNovoEvento').addEventListener('click', function() {
    let data = new Date().toISOString().slice(0, 10);

    abrirModalCriarEvento(data);
    });

    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        themeSystem: 'bootstrap5',
        initialView: 'dayGridMonth',
        locale: 'pt-br',
        headerToolbar: {
            left: 'prev',
            center: 'title',
            right: 'next'
        },
        dateClick: function(info) {
            //Abre o modal, e preenche a data com o dia clicado
            abrirModalCriarEvento(info.dateStr);
        },
        eventClick: function(info) {
            //Ao clicar no evento pega os dados e mostra

            eventoSelecionado = info.event //salvo o evento para usar depois
            const evento = info.event.extendedProps;

            document.getElementById('visualizarTitulo').textContent = info.event.title;
            document.getElementById('visualizarDescricao').textContent = evento.descricao || '(sem descrição)';
            document.getElementById('visualizarData').textContent = evento.data || '(sem data)';
            document.getElementById('visualizarInicio').textContent = evento.horario_inicio || '(sem horário)';
            document.getElementById('visualizarFim').textContent = evento.horario_fim || '(sem horário)';

            const modalVisualizar = new bootstrap.Modal(document.getElementById('modalVisualizarEvento'));
            modalVisualizar.show();
        },

        events: '/home/calendario/api/eventos'  //rota que vai devolver JSON com eventos do usuário
    });

    calendar.render();

    // BOTÃO SALVAR tanto post quanto put
    document.querySelector('.modal-body button.btn-primary').addEventListener('click', function(){
        const titulo = document.getElementById('titulo').value;
        const descricao = document.getElementById('descricao').value;
        const data = document.getElementById('data').value;
        const horario_inicio = document.getElementById('horario_inicio').value;
        const horario_fim = document.getElementById('horario_fim').value;

        let evento = {
            titulo: titulo,
            descricao: descricao,
            data: data,
            horario_inicio: horario_inicio,
            horario_fim: horario_fim
        }

        const url = modoEdicao
            ? `${window.origin}/home/calendario/api/eventos/${eventoSelecionado.id}`
            : `${window.origin}/home/calendario/api/eventos`;
        
        const metodo = modoEdicao ? 'PUT' : 'POST';

        fetch(url, {
            method: metodo,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(evento),
            credentials: 'include',
            cache: 'no-cache'
        })
        .then(function(respostaHttp){  //Oobjeto da resposta da requisição feita pelo front-end ao servidor (HTTP Response), basicamente pega os dados do front-end em http.

            return respostaHttp.json() //Converte a requisição http em objeto json
        })
        .then(function(respostaJson){ //resultado da conversão do JSON enviado pelo servidor (back-end), basicamente é a resposta do back-end ao receber os dados

            if(respostaJson.status == 'success'){
                modalEvento.hide();
                calendar.refetchEvents(); //Recarrega o calendario
            } else{
                alert('Erro: ' + respostaJson.message);
            };
        })
        .catch(function(erroConexao){
            console.error('Erro ao salvar evento:', erroConexao);
            alert('Erro de conexão.');
        })
    });

    //DELETE deleta um evento do calendar
    document.getElementById('btnExcluirEvento').addEventListener('click', function(){
        if(!eventoSelecionado) return; //Ou seja se for null o evento, só retorna nada
    
        fetch(`${window.origin}/home/calendario/api/eventos/${eventoSelecionado.id}`, {
        method: 'DELETE'
      })
        .then(function(respostaHttp){
            return respostaHttp.json()
        })
        .then(function(respostaJson){
            if(respostaJson.status === 'success'){
                calendar.refetchEvents()
                bootstrap.Modal.getInstance(document.getElementById('modalVisualizarEvento')).hide();
            } else{
                alert('Erro'+respostaJson.message)
            }
        })
        .catch(function(erroConexao){
                console.error('Erro ao criar evento:', erroConexao);
                alert('Erro de conexão.');
        })
    })

    // PUT edição do evento
    document.getElementById('btnEditarEvento').addEventListener('click', function () {
        if (!eventoSelecionado) return;

        document.getElementById('titulo').value = eventoSelecionado.title;
        document.getElementById('data').value = eventoSelecionado.extendedProps.data;
        document.getElementById('descricao').value = eventoSelecionado.extendedProps.descricao || '';
        document.getElementById('horario_inicio').value = eventoSelecionado.extendedProps.horario_inicio || '';
        document.getElementById('horario_fim').value = eventoSelecionado.extendedProps.horario_fim || '';

        modoEdicao = true

        //Fecha o modal de visualização
        bootstrap.Modal.getInstance(document.getElementById('modalVisualizarEvento')).hide();

        //Abre o modal de formulário, no caso o da a edição
        modalEvento.show();
    })
});
