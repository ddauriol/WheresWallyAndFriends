import json
import os


class Responses():
    def __init__(self, json_folder: str, json_response: str):
        self.json_folder: str = json_folder
        self.json_response: str = json_response
        self.file: str = self.json_folder + self.json_response
        self.responses: list = []
        self.active_response: list = []

    def get_response(self, place: int):
        with open(self.file, "r") as f:
            self.responses = json.load(f)
        for response in self.responses:
            if response['place'] == place:
                self.active_response = response['person']

    def check_response(self, grid: str):
        for response in self.active_response:
            if response['poss'] == grid:
                return response


class Users():
    def __init__(self, json_folder: str, json_users: str):
        self.json_folder: str = json_folder
        self.json_users: str = json_users
        self.file: str = self.json_folder + self.json_users
        self.users: list = []

    def file_exist(self):
        if os.path.exists(self.file):
            pass
        else:
            self.white_file()

    def white_file(self):
        with open(self.file, "w", encoding='utf-8') as f:
            json.dump(self.users, f)

    def check_exist_user(self, user_name: str):
        self.get_users()
        for user in self.users:
            if user['user_name'] == user_name.upper():
                return True
        return False

    def get_users(self):
        self.file_exist()
        with open(self.file, "r", encoding='utf-8') as f:
            self.users = json.load(f)

    def add_users(self, user_name: str, points: int):
        if self.check_exist_user(user_name) is False:
            self.users.append({
                'user_name': user_name.upper(),
                'points': points})
            self.white_file()

    def remove_user(self, user_name: str):
        for user in self.users:
            if user['user_name'] == user_name.upper():
                self.users.remove(user)
                self.white_file()

    def plus_points(self, user_name: str, points: int):
        if self.check_exist_user(user_name) is True:
            for user in self.users:
                if user['user_name'] == user_name.upper():
                    user['points'] = user['points'] + points
                    self.white_file()

    def clear_users(self):
        self.users = []
        self.white_file()


class Board():
    def __init__(self, json_folder: str, json_game: str):
        self.json_folder: str = json_folder
        self.json_game: str = json_game
        self.file: str = self.json_folder + self.json_game
        self.active_place: int = 0
        self.games: list = []
        self.read_game()

    def file_exist(self):
        if os.path.exists(self.file):
            pass
        else:
            self.white_file()

    def white_file(self):
        with open(self.file, "w", encoding='utf-8') as f:
            json.dump(self.games, f)

    def new_game(self, place: int = 1):
        self.games = [place]
        self.white_file()
        self.active_place = place

    def read_game(self):
        self.file_exist()
        with open(self.file, "r", encoding='utf-8') as f:
            self.games = json.load(f)
        self.active_place = self.games[0]

    def change_place(self, place: int):
        self.file_exist()
        self.games = [place]
        self.active_place = place
        self.white_file()

    def clear_game(self):
        self.new_game(0)
