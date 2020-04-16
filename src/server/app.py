from threading import Lock
from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, send, emit

from jsonmanager import Responses, Users, Board

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'whereswallyandfriends'
socketio = SocketIO(app, cors_allowed_origins="*")

json_folder = './json/'
json_response = 'response.json'
json_users = 'user.json'
json_game = 'games.json'

users = Users(json_folder, json_users)
board = Board(json_folder, json_game)
responses = Responses(json_folder, json_response)

# TEMP
board.new_game(1)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def player_connected():
    emit('status_msg', "Conectado")


@socketio.on('new_player')
def new_player(user_name):
    print(user_name)
    try:
        users.add_users(user_name, 0)
        emit('status_msg', f"{user_name} entrou no jogo",
             broadcast=True)
    except EnvironmentError:
        emit('erro_msg', 'Impossível entrar no jogo')


@socketio.on('start_game')
def start_game(place):
    try:
        board.new_game(int(place))
        print('Jogo iniciado: place ' + str(place))
        emit('started_game', board.active_place)
    except EnvironmentError:
        emit('erro_msg', 'Impossível iniciar o jogo')


@socketio.on('check_response')
def check_response(data):
    grid, user_name = data.split(';')
    print('O usuário: ' + user_name + ' clicou em: ' + grid)
    responses.get_response(board.active_place)
    response = responses.check_response(grid)
    if response is None:
        pass
    else:
        users.plus_points(user_name,
                          int(response['points']))
        emit('results',
             {'users': users.users,
              'user': user_name,
              'grid': grid},
             broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True, host="127.0.0.1")
