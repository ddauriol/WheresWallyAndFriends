from tinydb import TinyDB, Query


class RoomsManager():
    def __init__(self, storage_local):
        self.db_rooms = TinyDB(storage_local)
        self.rooms = Query()
        self.rooms_actives = []

    def CreateRoom(self, user_name, name_room, pass_room='123456'):
        json_schema = {'room_name': name_room,
                       'pass': pass_room,
                       'place_active': 0,
                       'places':
                           [
                               [1, 2, 3, 4, 5, 6, 7, 8, 9,
                                10, 11, 12, 13, 14, 15],
                               []
                            ], 'players': [{
                                'user_name': user_name,
                                'points': 0
                                }]}
        self.db_rooms.insert(json_schema)

    def GetRooms(self):
        query = self.db_rooms.search(self.rooms)
        for rooms in query:
            if 'room_name' in rooms:
                self.rooms_actives.append(rooms['room_name'])



storage_local = "./src/server/json/db_rooms.json"


rooms = RoomsManager(storage_local)
# rooms.CreateRoom("Elisa", "Familia", "abc")
# rooms.CreateRoom("Elisa", "Amigos", "abc")
print(rooms.rooms_actives)
rooms.GetRooms()
print(rooms.rooms_actives)
