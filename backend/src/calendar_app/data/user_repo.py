class UserRepo:
    def __init__(self):
        # simple in-memory store
        self.users = {}

    def get_all(self):
        return list(self.users.values())

    def get(self, user_id):
        return self.users.get(user_id)

    def save(self, user):
        self.users[user.id] = user
        return user

    def delete(self, user_id):
        return self.users.pop(user_id, None)