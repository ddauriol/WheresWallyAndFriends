import json


class Respostas():
    def __init__(self, json_folder, json_resposta):
        self.json_folder = json_folder
        self.json_resposta = json_resposta

    def getResposta(self, place):
        file = self.json_folder + self.json_resposta
        with open(file, "r") as f:
            data = json.load(f)
            respostas = data
        for resposta in respostas:
            if resposta['place'] == place:
                return resposta['person']


# json_folder = './src/server/json/'
# json_respostas = 'resposta.json'
# respostas = Respostas(json_folder, json_respostas)
# i = 1
# while(i < 16):
#     print(respostas.getResposta(i))
#     i = i + 1
