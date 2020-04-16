// Configuração do servidor
var ip_servidor = '127.0.0.1'
var port_servidor = '5000'

// Estabelecendo uma conexão
var socket = io.connect('http://' + ip_servidor + ':' + port_servidor);

// Variaveis gerais
const input_user_name = document.getElementById('input_user_name')
var user_name = input_user_name.value
const success_alert = document.getElementById('success-alert')
const btn_entrar = document.getElementById('btn_entrar')
const alert_danger = document.getElementById('alert-danger')
const msg_error = document.getElementById('msg_error')
const msg_sucess = document.getElementById('msg_sucess')

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
    console.log(place)
    if (place < 10){
        var place_str = '0' + String(place)
        div_pricipal.style.backgroundImage = 'url(/static//img/places/wally_place_' + place_str + '.jpg)'
    }else{
        div_pricipal.style.backgroundImage = 'url(/static//img/places/wally_place_' + place + '.jpg)'
    }
})

socket.on('status_msg', function (msg) {
    show_msg('status_msg', msg)
})

function show_msg(tipo='status_msg', msg=''){
    if (tipo == 'status_msg'){
        msg_sucess.innerHTML = msg
        success_alert.style.display = "block"
        setTimeout(function () {
            success_alert.style.display = 'none';
        }, 2000);
        return false;
    }
    if (tipo == 'erro_msg'){
        msg_sucess.innerHTML = msg
        success_alert.style.display = "block"
        setTimeout(function () {
            success_alert.style.display = 'none';
        }, 2000);
        return false;
    }
}

// Criando Grid
var div_pricipal = document.getElementById("div_principal")
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
        socket.emit('new_player', user_name)
        input_user_name.disabled = 'disabled'
        btn_entrar.disabled = 'disabled'
    }
}

function create_game(place){
    socket.emit('start_game', place)
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
    if(TextId.substring(0, 4) == 'grid'){
        socket.emit('check_response', TextId + ';' + user_name)
    }
}, false);

CreateGrid()