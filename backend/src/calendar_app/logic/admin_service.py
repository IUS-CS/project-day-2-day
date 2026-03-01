from calendar_app.data.user_model import User
from calendar_app.data.profile_model import UserProfile

class AdminService:
    def __init__(self, user_repo, profile_repo):
        self.user_repo = user_repo
        self.profile_repo = profile_repo

    def get_all_users(self):
        # Return all users stored in the repo
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def update_role(self, user_id, new_role):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        user.role = new_role
        self.user_repo.save(user)
        return user