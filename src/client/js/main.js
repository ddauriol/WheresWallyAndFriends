// Configuração do servidor
var ip_servidor = '127.0.0.1'
var port_servidor = '5000'

// Estabelecendo uma conexão
var socket = io.connect('http://' + ip_servidor + ':' + port_servidor);

// Returno da confirmação da conexão, mostra um alerta na tela.
socket.on('connect', function () {
    success_alert = document.getElementById('success-alert')
    success_alert.style.display = "block"
    setTimeout(function () {
        success_alert.style.display='none';
    }, 3000);
    return false;
});


// Criando Grid
var div_pricipal = document.getElementById("div_principal")
function CreateGrid(){
    var htmlOut = ''
    var htmlRow = ''
    i = 1
    while (i < 22){
        htmlRow = `<div class='row' id='row_${i}'>`
        j = 1
        while (j < 22){
            htmlRow += `<div class="gameGrid" id='grid_${i}_${j}'></div>`
            j++
        }
        htmlRow += `</div>`
        htmlOut += htmlRow
        i++
    }
    div_pricipal.innerHTML = htmlOut
}

// Monitorando clicks
document.addEventListener('click', function(e) {
    e = e || window.event;
    var target = e.target || e.srcElement,
        TextId = target.id;
    console.log(TextId)
    socket.emit('verifica_resposta', TextId)
}, false);

CreateGrid()