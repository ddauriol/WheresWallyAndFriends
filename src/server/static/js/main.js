// Configuração do servidor
var ip_servidor = '127.0.0.1'
var port_servidor = '5000'

// Estabelecendo uma conexão
var socket = io.connect('http://' + ip_servidor + ':' + port_servidor);

// Variaveis gerais
var place_active = 0
const input_user_name = document.getElementById('input_user_name')
const div_pricipal = document.getElementById("div_principal")
const success_alert = document.getElementById('success-alert')
const btn_entrar = document.getElementById('btn_entrar')
const btn_sair = document.getElementById('btn_sair')
const danger_alert = document.getElementById('danger-alert')
const msg_error = document.getElementById('msg_error')
const msg_sucess = document.getElementById('msg_sucess')
const list_players = document.getElementById('list_players')
const form_person = document.getElementById('form_person')
const tbody_finish = document.getElementById('tbody_finish')
var user_name = input_user_name.value

// Returno da confirmação da conexão, mostra um alerta na tela.
socket.on('connect', function () {
    msg_sucess.innerHTML = 'Sucesso! Jogador conectado'
    success_alert.style.display = "block"
    setTimeout(function () {
        success_alert.style.display = 'none';
    }, 2000);
    return false;
});

socket.on('started_game', function (place) {
    if (place < 10){
        var place_str = '0' + String(place)
        div_pricipal.style.backgroundImage = 'url(/static//img/places/wally_place_' + place_str + '.jpg)'
    }else{
        div_pricipal.style.backgroundImage = 'url(/static//img/places/wally_place_' + place + '.jpg)'
    }
})

socket.on('status_msg', function (data) {
    show_msg('status_msg', data['msg'])
    if (data.hasOwnProperty('users')){
        update_players(data['users'])
    }
})

socket.on('new_player', function (data) {
    user_name = data['user_name']
    input_user_name.value = user_name
    input_user_name.disabled = 'disabled'
    btn_entrar.disabled = 'disabled'
})

socket.on('exit_player', function (data) {
    if (data['user_name'] == user_name){
        input_user_name.value = user_name
        input_user_name.disabled = ''
        btn_entrar.disabled = ''
    }
    show_msg('erro_msg', data['msg'])
    update_players(data['users'])
})

socket.on('results', function (data) {
    show_msg('status_msg', data['msg'])
    console.log(data)
    document.getElementById(data['grid']).classList.add('getPerson')
    update_players(data['users'])
})

socket.on('board_updated', function (data) {
    update_board(data)
})

socket.on('results_finish', function (result) {
    htmlOut = ''
    Object.entries(result).forEach(([key, user]) => {
        console.log(user)
        htmlOut += `
        <tr>
            <th scope="row">${key+1}</th>
            <td>${user['user_name']}</td>
            <td>${user['points']}</td>
        </tr>`
    })
    tbody_finish.innerHTML = htmlOut
    $('#result_modal').modal('show');
})

function show_msg(tipo='status_msg', msg=''){
    if (tipo == 'status_msg'){
        msg_sucess.innerHTML = msg
        success_alert.style.display = "block"
        setTimeout(function () {
            success_alert.style.display = 'none';
        }, 3000);
        return false;
    }
    if (tipo == 'erro_msg'){
        msg_error.innerHTML = msg
        danger_alert.style.display = "block"
        setTimeout(function () {
            danger_alert.style.display = 'none';
        }, 3000);
        return false;
    }
}

function update_players(users){
    var htmlOut = `
    <button id="btnGroupDrop1" type="button" class="btn btn-primary dropdown-toggle mr-3" data-toggle="dropdown"
    aria-haspopup="true" aria-expanded="false">
        Jogadores
    </button>
    <div class="dropdown-menu" aria-labelledby="btnGroupDrop1">`

    Object.entries(users).forEach(([key, user]) => {
        htmlOut += `
            <a class="dropdown-item" href="#">${user['user_name']}
            <span class="badge alert-primary">${user['points']}</span></a>
            `
    })

    htmlOut += `</div>`
    list_players.innerHTML = htmlOut
}

// Criando Grid
function CreateGrid() {
    var htmlOut = ''
    var htmlRow = ''
    i = 1
    while (i < 22) {
        htmlRow = `<div class='row' id='row_${i}'>`
        j = 1
        while (j < 22) {
            htmlRow += `<div class="gameGrid" id='grid_${i}_${j}'></div>`
            j++
        }
        htmlRow += `</div>`
        htmlOut += htmlRow
        i++
    }
    div_pricipal.innerHTML = htmlOut
}

function InToGame() {
    user_name = input_user_name.value
    if (user_name != '') {
        socket.emit('new_player', user_name);
    }else{
        show_msg('erro_msg', 'Escolha um nome de jogador')
    }
}

function create_game(place){
    socket.emit('start_game', place)
}

function exit_game(user_name){
    if (user_name != ''){
        socket.emit('exit_game', user_name)
    }
}

function update_board(data){
    htmlOut = ``
    Object.entries(data['responses']).forEach(([key, value]) => {
        htmlOut += `
        <button type="button" class="btn alert-primary ml-2">
            <img src="/static//img/person/${value['name'].toLowerCase()}.png") width="30" height="30"
                class="d-inline-block align-top ml-1">
            <span class="badge badge-light">${value['points']}</span>
        </button>`
    })
    form_person.innerHTML = htmlOut
    place = data['active_place']
    if (place < 10){
        var place_str = '0' + String(place)
        div_pricipal.style.backgroundImage = 'url(/static//img/places/wally_place_' + place_str + '.jpg)'
    }else{
        div_pricipal.style.backgroundImage = 'url(/static//img/places/wally_place_' + place + '.jpg)'
    }
    CreateGrid()
}

function check_update(){
    socket.emit('check_update')
}

// Monitorando clicks
document.addEventListener('click', function (e) {
    e = e || window.event;
    var target = e.target || e.srcElement,
        TextId = target.id;
    console.log(TextId)
    if (TextId == 'btn_entrar'){
        InToGame()
    }
    if (TextId == 'btn_sair'){
        exit_game(user_name)
    }
    if(TextId.substring(0, 4) == 'grid' && user_name != ''){
        if (document.getElementById(TextId).classList.contains('getPerson')){
            show_msg('erro_msg', 'Personagem já encontrado!')
        }else{
            socket.emit('check_response', TextId + ';' + user_name)
        }
    }
    if(TextId.substring(0, 4) == 'grid' && user_name == ''){
        show_msg('erro_msg', 'Entre no jogo!')
    }
}, false);

CreateGrid()