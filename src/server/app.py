from flask import Flask, request, jsonify
from flask_socketio import SocketIO, send, emit

import json
import time

from dbmanager import Places, Users
from jsonmanager import Respostas

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whereswallyandfriends'
socketio = SocketIO(app, cors_allowed_origins="*")

json_folder = './json/'
json_respostas = 'resposta.json'
json_users = 'user.json'
json_places = 'places.json'

respostas = Respostas(json_folder, json_respostas)
users = Users(json_folder + json_users)
places = Places(json_folder + json_places)
places.PurgeDB()
places.CreatPlace()


@socketio.on('connect')
def enviarDadosJogo():
    emit('jogador_conectado', "")


@socketio.on('verifica_resposta')
def verificaResposta(data):
    print(data)
    place = places.GetPlace()
    for plc in place:
        place_int = plc['active']
    print(respostas.getResposta(place_int))
    # emit('resultado',
    #      {'room': room, 'msg': msg_retorno},
    #      broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True, host="127.0.0.1")
