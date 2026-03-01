class ProfileRepo:
    def __init__(self):
        self.profiles = {}

    def get(self, user_id):
        return self.profiles.get(user_id)

    def save(self, profile):
        self.profiles[profile.user_id] = profile
        return profile

    def delete(self, user_id):
        return self.profiles.pop(user_id, None)