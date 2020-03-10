from copy import  deepcopy


class UserStore:

    def __init__(self):
        self._users = []
        self._next_id = 0

    def add_user(self, name: str, age: int, type: str):
        self._users.append({"id": self._next_id, "name": name, "age": age, "type": type})
        self._next_id += 1
        return self._next_id - 1

    def get_users(self):
        return deepcopy(self._users)
