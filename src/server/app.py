from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit

import json
import time

from jsonmanager import gameManager, respostaManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whereswallyandfriends'
socketio = SocketIO(app, cors_allowed_origins="*")

json_folder = './json/'
json_games = 'games.json'
json_respostas = 'resposta.json'

games = gameManager(json_folder, json_games)
respostas = respostaManager(json_folder, json_respostas)

@socketio.on('connect')
def enviarDadosJogo():
    emit('jogador_conectado', "")


@socketio.on('entrar_no_jogo')
def handleEntrarNoJogo(data):
    user_name, room = data.split(';')
    room = int(room)
    games.newPlayer(room, '127.0.0.1', user_name)
    gamesInfo = games.getGameInfo(room)
    emit('dados_do_jogo', gamesInfo)


if __name__ == '__main__':
    socketio.run(app, host="127.0.0.1")
