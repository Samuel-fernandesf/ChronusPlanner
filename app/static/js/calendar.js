document.addEventListener('DOMContentLoaded', function() {

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
            alert('Inside Clicked on: ' + info.dateStr);
            // Se clicou em um evento
            abrirModalVerEvento(info.event);
        },

        events: '/home/calendario/api/eventos'  // sua rota que vai devolver JSON com eventos do usuário
    });

    calendar.render();

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

        fetch(`${window.origin}/home/calendario/api/eventos`, {
            method: 'POST',
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
            console.error('Erro ao criar evento:', erroConexao);
            alert('Erro de conexão.');
        })
    });
});
