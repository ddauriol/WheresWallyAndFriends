from tinydb import TinyDB, Query


class Users():
    def __init__(self, storage_local):
        self.db_users = TinyDB(storage_local)
        self.user = Query()
        self.status = 1

    def InsertUser(self, user_name):
        json_schema = {"user_name": user_name,
                       "points": 0}
        users_actives = self.db_users.all()
        if users_actives == []:
            self.db_users.insert(json_schema)
            self.status = 1
        else:
            for user in users_actives:
                if user['user_name'] == user_name:
                    self.status = 0

            if self.status == 1:
                self.db_users.insert(json_schema)
                self.status = 1

    def UpadatePoints(self, user_name, points_plus):
        query = self.db_users.search(self.user.user_name == user_name)
        for user in query:
            points = user['points']
            points = int(points) + int(points_plus)
            self.db_users.update({"points": points},
                                 self.user.user_name == user_name)

    def PurgeDB(self):
        self.db_users.purge()


class Places():
    def __init__(self, storage_local):
        self.db_places = TinyDB(storage_local)
        self.place = Query()
        self.status = 1

    def CreatPlace(self):
        json_schema = {"active": 0}
        self.db_places.insert(json_schema)

    def NextPlace(self):
        places = self.db_places.all()
        for place in places:
            active_place = place['active']
            next_place = int(active_place) + 1
            if next_place < 15:
                self.db_places.update({"active": next_place},
                                     self.place.active == active_place)

    def PurgeDB(self):
        self.db_places.purge()


# storage_local = "./src/server/json/user.json"
# users = Users(storage_local)
# users.InsertUser("Mirna")
# users.InsertUser("ddauriol")
# users.UpadatePoints("Mirna", 5)


storage_local = "./src/server/json/places.json"
place = Places(storage_local)
place.CreatPlace()
place.NextPlace()
place.PurgeDB()
