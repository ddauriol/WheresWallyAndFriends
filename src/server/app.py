from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, emit
from jsonmanager import Responses, Users, Board

# settigns for Flask e Socketio
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'whereswallyandfriends'
socketio = SocketIO(app, cors_allowed_origins="*")

# Settings
json_folder = './json/'
json_response = 'response.json'
json_users = 'user.json'
json_game = 'games.json'

# var for games
users = Users(json_folder, json_users)
board = Board(json_folder, json_game)
responses = Responses(json_folder, json_response)
users.clear_users()

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def player_connected():
    emit('status_msg', "Conectado")


@socketio.on('exit_game')
def player_disconnected(user_name):
    users.remove_user(user_name)
    emit('exit_player',
         {'msg': f"Usuário {user_name} se desconectou.",
          'users': users.users,
          'user_name': user_name},
         broadcast=True)


@socketio.on('new_player')
def new_player(user_name):
    user_name = user_name.upper()
    try:
        users.add_users(user_name, 0)
        emit('status_msg', {'msg': f"{user_name} entrou no jogo",
                            'users': users.users},
             broadcast=True)
        emit('new_player', {'user_name': user_name})
    except EnvironmentError:
        emit('erro_msg', 'Impossível entrar no jogo')


@socketio.on('start_game')
def start_game(place):
    try:
        board.new_game(int(place))
        emit('started_game', board.active_place, broadcast=True)
        check_update()
    except EnvironmentError:
        emit('erro_msg', 'Impossível iniciar o jogo')


@socketio.on('check_response')
def check_response(data):
    grid, user_name = data.split(';')
    responses.get_response(board.active_place)
    response = responses.check_response(grid)
    if response is None:
        pass
    else:
        users.plus_points(user_name,
                          int(response['points']))
        person = response['name']
        emit('results',
             {'msg': f'O jogador {user_name} achou o personagem {person}',
              'users': users.users,
              'user': user_name,
              'grid': grid,
              'person': person},
             broadcast=True)
        plus_courent_points(int(response['points']))


@socketio.on('check_update')
def check_update():
    responses.get_response(board.active_place)
    emit('board_updated',
         {'responses': responses.active_response,
          'active_place': board.active_place},
         broadcast=True)


def plus_courent_points(num: int):
    board.courent_points = board.courent_points + num
    if board.courent_points == responses.max_points:
        board.courent_points = 0
        board.next_place()
        if board.active_place == 15:
            emit('results_finish', users.users, broadcast=True)
        else:
            board.change_place(board.active_place)
            check_update()


if __name__ == '__main__':
    socketio.run(app, debug=True, host="127.0.0.1")
