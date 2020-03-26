from tinydb import TinyDB, Query

db_rooms = TinyDB('./src/server/json/db_rooms.json')
rooms = Query()

db_rooms.insert({'name': 'John', 'age': 22})

print(db_rooms.search(rooms.name == 'John'))
